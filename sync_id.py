import requests
import os
from json import dumps
f = open('/home/pi/Desktop/EDGE/ID.txt','r')
id = f.read()
f.close()
payload = {'Device ID':id}
r = requests.post('http://api.frizzleweather.com/node/initialise',data=dumps(payload))

data = r.json()
print(data)
date = data['date']
time = data['time']

if 'Device ID' in data.keys():
	f = open('/home/pi/Desktop/EDGE/ID.txt','w')
	uid = data['Device ID']
	f.write(uid)
	f.close()
os.system('sudo timedatectl set-ntp false')
os.system('sudo timedatectl set-time \"{0} {1}\"'.format(date,time))

