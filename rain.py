import sys
from gpiozero import LightSensor

rain = LightSensor(18)
rain_value= 1 - rain.value
rain.close()

with open('/home/pi/Desktop/EDGE/rain.txt','w') as f:
	f.write(rain_value)
