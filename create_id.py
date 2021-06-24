import requests
import os
from json import dumps

#print(os.stat("/home/pi/Desktop/EDGE/test.txt").st_size == 0)
if os.stat('/home/pi/Desktop/EDGE/ID.txt').st_size == 0:
	r = requests.get('https://api.frizzleweather.com/node/create', verify = False)
	data = r.json()
	device_id = data['Device ID']
	print(device_id)
	f = open('/home/pi/Desktop/EDGE/ID.txt','w')
	f.write(device_id)
	f.close()
