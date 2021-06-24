#!/bin/sh

export PATH="/usr/bin/python2.7:$PATH"

Connect(){
	sudo pon rnet
	echo Connecting to the internet...
	sleep 1m
	echo Connected
}

Working(){
	python /home/pi/Desktop/EDGE/sync_id.py
	while true
 	do
 		python /home/pi/Desktop/EDGE/frizzle.py
 		sleep 30
 	done
}


#/sbin/ifconfig ppp0
echo configuring network
sleep 2m
path=$(curl -k -X GET "https://api.frizzleweather.com/node/server/status")
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
