from subprocess import Popen
import subprocess
import os


class VideoPlayer:
    def __init__(self):
        self.current_video = None
        self.path_to_video = None
        self.video_is_playing = False
        self.player = None
        self.video_is_stopped = True

    def set_video(self, path):
        self.path_to_video = path
        splited_path = path.split(os.path.sep)
        self.current_video = splited_path[len(splited_path)-1]

    def play_video(self):
        self.player = Popen(['omxplayer', '-o', 'hdmi', '-b', self.path_to_video], shell=False)
        self.video_is_playing = True
        self.video_is_stopped = False

    def stop_video(self):
        if not self.video_is_stopped:
            os.system('killall omxplayer.bin')
            self.video_is_playing = False
            self.video_is_stopped = True
            self.player = None
