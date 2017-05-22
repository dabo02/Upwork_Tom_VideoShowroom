from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from werkzeug.utils import secure_filename
from threading import Thread
from VideoPlayer import VideoPlayer
import RPi.GPIO as GPIO
import os

app = Flask(__name__)


UPLOAD_FOLDER = '/home/dabo02/Desktop/Projects/Side_Projects/Upwork_Tom_VideoShowroom/static/videos/'
ALLOWED_EXTENSIONS = set(['mp3', 'mp4'])
light_state = False
exit_flag = False
current_video = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_for_current():
    global current_video
    if not current_video:
        current_video = os.listdir(UPLOAD_FOLDER)[0]


def main_routine():
    GPIO.setMode(GPIO.BCM)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12, GPIO.OUT)
    vp = VideoPlayer()
    global current_video
    while True:
        if GPIO.input(11) and not vp.video_is_playing:
            GPIO.output(12, 1)
            check_for_current()
            vp.set_video(current_video)
            vp.play_video()
        elif not GPIO.input(11) and vp.video_is_playing:
                vp.stop_video()
                GPIO.output(12, 0)


@app.route('/')
def dashboard():
    video_list = os.listdir(UPLOAD_FOLDER)
    video_info = {}
    videos = []
    i = 0
    global current_video
    for v in video_list:
        if current_video:
            if current_video in v:
                current = True
            else:
                current = False
        else:
            current = False
        i = i+1
        name = v.rsplit('.', 1)[0]
        video_info = {'name': name, 'id': v, 'current': current}
        videos.append(video_info)
    return render_template('index.html', videos=videos)


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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('dashboard', filename=filename))


@app.route('/remove_video/<id>', methods=['GET'])
def remove_video(id):
    video_to_remove = UPLOAD_FOLDER + '/' + id
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], video_to_remove))
    return redirect(url_for('dashboard'))

@app.route('/update_video/<id>', methods=['GET'])
def change_current_video(id):
    new_video = id
    global current_video
    current_video = UPLOAD_FOLDER + '/' + new_video
    return redirect(url_for('dashboard'))




@app.route('/light_state', methods=['POST'])
def light_state():
    state = request.light_state
    if state:
        # TODO set RPI GPIO to HIGH
        # TODO start video and set lighting a to lighting_lvl and lighting_color
        return
    # TODO set RPI GPIO to LOW

    # TODO stop video, reset and turn of lighting



if __name__ == '__main__':
    loop_thread = Thread(target=main_routine())
    loop_thread.start()
    app.run(host='localhost', port=3000)
