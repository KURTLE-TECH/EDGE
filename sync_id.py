import requests
import os
from json import dumps
f = open('/home/pi/Desktop/edge/ID.txt','r')
id = f.read()
f.close()
payload = {'Device ID':id}
r = requests.post('http://13.126.242.56:80/register_node',data=dumps(payload))

data = r.json()
print(data)
date = data['date']
time = data['time']

if 'id' in data.keys():
	f = open('/home/pi/Desktop/edge/ID.txt','w')
	uid = data['id']
	f.write(uid)
	f.close()
os.system('sudo timedatectl set-ntp false')
os.system('sudo timedatectl set-time \"{0} {1}\"'.format(date,time))

