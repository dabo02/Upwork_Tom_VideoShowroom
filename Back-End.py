from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from celery import Celery
from werkzeug.utils import secure_filename
from VideoPlayer import VideoPlayer
import RPi.GPIO as GPIO
import os

app = Flask(__name__)
local = True
if local:
    UPLOAD_FOLDER = '/home/dabo02/Desktop/Projects/Side_Projects/Upwork_Tom_VideoShowroom/static/video/'
else:
    UPLOAD_FOLDER='/home/pi/Downloads/'

app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

ALLOWED_EXTENSIONS = set(['mp3', 'mp4'])
light_state = False
exit_flag = False
current_video = None
preview_video = ''

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.OUT)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_for_current():
    global current_video
    if not current_video:
        current_video = os.listdir(UPLOAD_FOLDER)[0]


@celery.task
def main_routine():
    vp = VideoPlayer()
    global current_video
    while True:
        if not GPIO.input(23):
            if not vp.video_is_playing:
                GPIO.output(24, 0)
                check_for_current()
                vp.set_video(current_video)
                vp.play_video()
        else:
            vp.stop_video()
            GPIO.output(24, 1)


@app.route('/')
def dashboard():
    task = main_routine.apply_async()
    video_list = os.listdir(UPLOAD_FOLDER)
    video_info = {}
    videos = []
    i = 0
    global current_video
    global preview_video
    global light_state
    for v in video_list:
        if current_video:
            if current_video in v:
                current = True
            else:
                current = False
        else:
            current = False

        if preview_video:
            if preview_video in v:
                preview = v
        else:
            preview = ''
        name = v.rsplit('.', 1)[0]
        video_info = {'name': name, 'id': v, 'current': current}
        videos.append(video_info)
        i = i+1

    return render_template('index.html', videos=videos, preview=preview, light_state=light_state)


@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        flash('No file part')
        return redirect(url_for('dashboard'))
    file = request.files['video']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('dashboard'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)


@app.route('/remove_video/<id>', methods=['GET'])
def remove_video(id):
    video_to_remove = UPLOAD_FOLDER + '/' + id
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], video_to_remove))
    return redirect(url_for('dashboard'))

@app.route('/update_video/<id>', methods=['GET'])
def change_current_video(id):
    new_video = id
    global current_video
    current_video = new_video
    return redirect(url_for('dashboard'))


@app.route('/preview_video/<id>', methods=['GET'])
def preview_current_video(id):
    global preview_video
    preview_video = id
    return redirect(url_for('dashboard'))

@app.route('/light_state/<state>', methods=['GET'])
def light_state(state):
    global light_state
    if state in 'True':
        GPIO.output(24, 1)
        light_state = True
        return redirect(url_for('dashboard'))
    GPIO.output(24, 0)
    light_state = False
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    if local:
        app.run(host='localhost', port=3200)
    else:

        app.run(host='0.0.0.0', port=3500)
