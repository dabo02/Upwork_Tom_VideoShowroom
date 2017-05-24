from subprocess import Popen
import os


class VideoPlayer:
    def __init__(self):
        self.current_video = None
        self.path_to_video = None
        self.video_is_playing = False
        self.player = None

    def set_video(self, path):
        self.path_to_video = path
        splited_path = path.split(os.path.sep)
        self.current_video = splited_path[len(splited_path)-1]
        return True

    def play_video(self):
        os.system('killall omxplayer.bin')
        self.player = Popen(['omxplayer', '-b', self.path_to_video], shell=False)
        self.video_is_playing = True
        return True

    def stop_video(self):
        os.system('killall omxplayer.bin')
        self.player = None
