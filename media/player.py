import sys, subprocess
from urllib.error import URLError

class AmbiencePlayer():
    def __init__(self, target_file_path):
        self.playing = False
        self.target_file_path = target_file_path
        self.process = None

    def Play_music(self):
        try:
            if not self.playing:
                self.process = subprocess.Popen(['mpv', '--loop-file=inf', '--no-video', '--no-audio-display','--no-terminal',self.target_file_path], stdout=subprocess.PIPE,text = True)
                self.playing = True
        except FileNotFoundError:
            print('cannot find the file please give correct file path')
    def stop(self):
        if self.process:
            if self.process.poll() is None and self.playing:
                self.process.kill()
                self.process.wait()
                print("process ended exitCode: ",self.process.returncode)
                self.playing = False
            else:
                print("nothing is playing")






class VideoPlayer():
    def __init__(self):
        self.playing = False
        self.process = None


    def play(self, video_url:str, audio_url:str):

        command = ['mpv', video_url, f'--audio-file={audio_url}', '--no-terminal']
        try:
            if not self.playing:
                self.process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
                self.playing = True

        except FileNotFoundError:
            print("mpv is not installed please install it first")


    def stop(self):
        if self.process:
            if self.process.poll() is None and self.playing:
                self.process.kill()
                self.process.wait()
                self.playing = False

                print('Process ended with exitCode:', self.process.returncode)
            else:
                print("nothing is playing")






if __name__=="__main__":
    player = AmbiencePlayer("/home/nirav/Music/POP/sombr - back to friends.flac")
    player.Play_music()
    # confirm you can hear it
    input("press enter to stop")
    player.stop()