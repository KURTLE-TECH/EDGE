import requests
import os
from json import dumps
from time import sleep

def verify_id():
	f = open("/home/pi/Desktop/EDGE/ID.txt","r")
	id = f.read()
	f.close()
	payload = {'Device ID':id}
	print(payload)
	r = requests.post('https://api.frizzleweather.com/node/initialise',verify=False, data = dumps(payload))
	data = r.json()
	print(data)
	if 'date' in data.keys():
		date = data['date']
		#print(date)
		time = data['time']
		#print(time)
		os.system('sudo timedatectl set-ntp false')
		os.system('sudo timedatectl set-time \"{0} {1}\"'.format(date,time))
		#print('cool')
		return [date,time]
	else:
		print('trying again')
		sleep(3)
		verify_id()

verify_id()

