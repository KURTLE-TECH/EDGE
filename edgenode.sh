
export PATH="/usr/bin/python2.7:$PATH"
sudo pon rnet;
python /home/pi/Desktop/edge/sync_server.py;

while true;
do
python /home/pi/Desktop/edge/camqtt_log.py;
sleep 30;
done
