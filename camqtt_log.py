import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import smbus
import time
from ctypes import c_short
import base64
import sys
import Adafruit_DHT
from picamera import PiCamera
import psutil
import datetime
#from firebase import firebase
from gpiozero import LightSensor, InputDevice

#firebase = firebase.FirebaseApplication('https://frizzle-b5c32-default-rtdb.firebaseio.com/', None)

MQTT_server = '13.126.242.56'
MQTT_path1 = "Frizzle/Sensor_Data"
MQTT_path2 = "Frizzle/Edge_logs" 
DEVICE  = 0x77 
 

bus = smbus.SMBus(1) 
 
def convertToString(data):
  # Simple function to convert binary data into
  # a string
  return str((data[1] + (256 * data[0])) / 1.2)

def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index] << 8) + data[index + 1]).value

def getUshort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index] << 8) + data[index + 1]

def readBmp180Id(addr=DEVICE):
  # Chip ID Register Address
  REG_ID     = 0xD0
  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)
  
def readBmp180(addr=DEVICE):
  # Register Addresses
  REG_CALIB  = 0xAA
  REG_MEAS   = 0xF4
  REG_MSB    = 0xF6
  REG_LSB    = 0xF7
  # Control Register Address
  CRV_TEMP   = 0x2E
  CRV_PRES   = 0x34 
  # Oversample setting
  OVERSAMPLE = 3    # 0 - 3
  
  # Read calibration data
  # Read calibration data from EEPROM
  cal = bus.read_i2c_block_data(addr, REG_CALIB, 22)

  # Convert byte data to word values
  AC1 = getShort(cal, 0)
  AC2 = getShort(cal, 2)
  AC3 = getShort(cal, 4)
  AC4 = getUshort(cal, 6)
  AC5 = getUshort(cal, 8)
  AC6 = getUshort(cal, 10)
  B1  = getShort(cal, 12)
  B2  = getShort(cal, 14)
  MB  = getShort(cal, 16)
  MC  = getShort(cal, 18)
  MD  = getShort(cal, 20)

  # Read temperature
  bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
  time.sleep(0.005)
  (msb, lsb) = bus.read_i2c_block_data(addr, REG_MSB, 2)
  UT = (msb << 8) + lsb

  # Read pressure
  bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
  time.sleep(0.04)
  (msb, lsb, xsb) = bus.read_i2c_block_data(addr, REG_MSB, 3)
  UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

  # Refine temperature
  X1 = ((UT - AC6) * AC5) >> 15
  X2 = (MC << 11) / (X1 + MD)
  B5 = X1 + X2
  temperature = int(B5 + 8) >> 4

  # Refine pressure
  B6  = B5 - 4000
  B62 = int(B6 * B6) >> 12
  X1  = (B2 * B62) >> 11
  X2  = int(AC2 * B6) >> 11
  X3  = X1 + X2
  B3  = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

  X1 = int(AC3 * B6) >> 13
  X2 = (B1 * B62) >> 16
  X3 = ((X1 + X2) + 2) >> 2
  B4 = (AC4 * (X3 + 32768)) >> 15
  B7 = (UP - B3) * (50000 >> OVERSAMPLE)

  P = (B7 * 2) / B4

  X1 = (int(P) >> 8) * (int(P) >> 8)
  X1 = (X1 * 3038) >> 16
  X2 = int(-7357 * P) >> 16
  pressure = int(P + ((X1 + X2 + 3791) >> 4))

  return (temperature/10.0,pressure/100.0)

def readDHT():
    try:
	humidity, temp = Adafruit_DHT.read_retry(11,17)
    	#print('The temperature is: ',temperature,'and the humidity is: ',humidity,'%')
    	#time.sleep(1)
    	return [humidity, temp]
    except: 
	return [0,0]
    
def readcamera():
    try:
    	camera = PiCamera()
    	camera.resolution = (256, 256)
    	#camera.framerate(15)
    	camera.start_preview()
    	time.sleep(1)
    	camera.capture('/home/pi/Desktop/Nubius_Pics/image.jpg')
    	camera.stop_preview()
    	with open('/home/pi/Desktop/Nubius_Pics/image.jpg','rb') as img_file:
     		my_string = base64.b64encode(img_file.read())
        	fileContent = img_file.read()
        	bytearr = bytearray(fileContent)
    	return str(my_string)
    except:
	return 0

def ldr():
    try:
    	light = LightSensor(4)
    	return light.value
    except:
	return 0

def rainy():
    try:
    	rain = InputDevice(18)
    	if not rain.is_active:
        	return 1
   	else:
        	return 0
    except:
	return 'err'

def stats():
    
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    
    return ram, cpu

def on_connect(client, userdata, flags, rc):
    print("connected with code "+str(rc))
    
def on_message(client, userdata, msg):
    print('message received from '+str(msg.topic)+' : '+str(msg.payload))

def main():    
  (ram,cpu) = stats()
  DHTT = readDHT()
  cam = readcamera()
  (temperature,pressure)=readBmp180()
  light = ldr()
  rain = rainy()
  x = str(datetime.datetime.now())
  f = open('/home/pi/Desktop/EDGE/ID.txt','r')
  id = f.read()
  f.close()
  
  #payload
  data = {'Device ID': id,
          'TimeStamp': x,
          'Light':str(light),
          'Temperature':str(DHTT[1]),
          'Pressure': str(pressure),
          'Humidity': str(DHTT[0]),
          'Rain' : str(rain),
          'picture': cam}
  stat = {'RAM': str(ram), 'CPU': str(cpu)}
  for i in data:
	if data[i] == 'None':
		stat[str(i)] = 'wiring error'
  print(data)
  print(pressure)
  data2 = {'rishi':'PESu'}
  print(stat)
  print(sys.getsizeof(cam))
  
  #client config
  client = mqtt.Client("pi")
  client.username_pw_set('frizzle_test','FRIZZLE')
  client.on_connect = on_connect
  client.on_message = on_message
  
  #client connection and comms
  client.connect(MQTT_server,1883)
  client.publish(MQTT_path1,str(data))
  publish.single(MQTT_path1, str(data),hostname=MQTT_server, auth={'username':"frizzle_test",'password':"FRIZZLE"} )
  #client.publish(MQTT_path2,str(data2))
  #client.loop_forever()
  #client.disconnect()
  
  #storing data locally
 # f = open('model_tests.txt','a')
 # f.write('\n'+str(data))
 # f.close()
  
  
if __name__=="__main__":
       main()

