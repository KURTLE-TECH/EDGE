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
 	python /home/pi/Desktop/EDGE/frizzle.py
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
	sleep 1m
	sudo poff rnet
	sleep 1m
	sudo reboot
else
	echo connected
	Working
	sleep 1m
	sudo poff rnet
	sleep 1m
	sudo reboot
fi
