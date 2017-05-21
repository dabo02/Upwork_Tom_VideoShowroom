from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import requests
import socket as s
import os
app = Flask(__name__)


UPLOAD_FOLDER = '/home/dabo02/Desktop/Projects/Side_Projects/Upwork_Tom_VideoShowroom/static/videos/'
ALLOWED_EXTENSIONS = set(['mp3', 'mp4'])
lighting_lvl = None
lighting_color = None
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def dashboard():
    videos = app.config['UPLOAD_FOLDER']
    return render_template('index.html')


@app.route('/upload_video', methods=['POST'])
def upload_video():
    req = request
    if 'video' not in request.files:
        # flash('No file part')
        return redirect(url_for(''))
    file = request.files['video']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('', filename=filename))

@app.route('/remove_video/<id>', methods=['DELETE'])
def remove_video(id):
    video_to_remove = UPLOAD_FOLDER + '/' + id
    # TODO remove video logic

@app.route('/update_video', methods=['PUT'])
def change_current_video():
    new_video = request.video_name
    new_video_path = UPLOAD_FOLDER + '/' + new_video
    # TODO update new video


@app.route('/lid', methods=['POST'])
def lid_state():
    lid_state = request.lid_state
    if lid_state:
        # TODO start video and set lighting a to lighting_lvl and lighting_color
        return

    # TODO stop video, reset and turn of lighting


if __name__ == '__main__':
    app.run(host='localhost', port=2500)
