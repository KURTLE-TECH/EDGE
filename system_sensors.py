import RPi.GPIO as GPIO

def getPinFunctionName(pin):
	functions = {GPIO.IN: 'Input',
		     GPIO.OUT: 'Output',
		     GPIO.I2C: 'I2C',
	 	     GPIO.SPI: 'SPI',
		     GPIO.HARD_PWM: 'HARD_PWM',
		     GPIO.SERIAL: 'Serial',
		     GPIO.UNKNOWN: 'Unknown'}
	return functions[GPIO.gpio_function(pin)]

gpio = [i for i in range(1,28)]
GPIO.setmode(GPIO.BCM)
for pin in gpio:
	print("GPIO %s is an %s" % (pin,getPinFunctionName(pin)))
