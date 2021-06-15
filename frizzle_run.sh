#!/bin/sh

export PATH="/usr/bin/python2.7:$PATH"

Connect(){
	sudo pon rnet
	echo Connecting to the internet...
	sleep 1m
	echo Connected
}

Working(){
	python /home/pi/Desktop/EDGE/create_id.py
	sleep 1m
	python /home/pi/Desktop/EDGE/sync_id.py
	python /home/pi/Desktop/EDGE/rain.py
	while true
 	do
 		python /home/pi/Desktop/EDGE/frizzle.py
 		sleep 30
 	done
}


#/sbin/ifconfig ppp0
path=$(curl -X GET "http://13.126.242.56:80/node/server/status")
echo $path
if [ -z "$path" ]; 
then
	echo not connected
	Connect
	Working
else
	echo connected
	Working
fi
