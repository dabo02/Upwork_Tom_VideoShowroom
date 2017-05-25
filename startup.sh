python3 /home/pi/Desktop/Upwork_Tom_VideoShowroom/Back-End.py > /tmp/flask-server-log.txt &

sleep 3
cd /home/pi/Desktop/Upwork_Tom_VideoShowroom

celery worker -A Back-End.celery > /tmp/celery-worker-log.txt &

sleep 3
#sleep 1

#while ! grep -m1 '.> celery           exchange=celery(direct) key=celery'; do
#	sleep 1
cd /home/pi/
echo 'Everything started succesfully'
echo continue

