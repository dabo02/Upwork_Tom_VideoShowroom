from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import socket as s
import os
app = Flask(__name__)


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def dashboard():

    return render_template('index.html')


@app.route('/change_lighting', methods='POST')
def light_change():
    dim = request.dimlvl
    color = request.color


@app.route('/upload_video', methods='POST')
def upload_video():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))

@app.route('/remove_video/<id>', methods='DELETE')
def remove_video(id):


@app.route('/update_video', methods='PUT')
def change_current_video():
    new_video = request.video_name
    new_video_path = UPLOAD_FOLDER + '/' + new_video

@app.route('/')
def


if __name__ == '__main__':
    app.run()
