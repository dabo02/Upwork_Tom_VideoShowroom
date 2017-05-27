#!/bin/bash
# /etc/init.d/startup

### BEGIN INIT INFO
# Provides:          startup
# Required-Start:    $ALL
# Required-Stop:
# Default-Start:     2 3 5
# Default-Stop:      0 1 6
# Short-Description: Run Video Player as Daemon
# Description:       This script starts the server and worker for the Video Player App
### END INIT INFO

python3 /home/pi/Desktop/Upwork_Tom_VideoShowroom/Back-End.py &

sleep 3
cd /home/pi/Desktop/Upwork_Tom_VideoShowroom

celery worker -A Back-End.celery &

sleep 3
#sleep 1

#while ! grep -m1 '.> celery           exchange=celery(direct) key=celery'; do
#	sleep 1

echo 'Everything started succesfully'
echo continue

