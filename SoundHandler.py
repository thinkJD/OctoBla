# ---------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jd.georgens@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return.
#                                                        Jan-Daniel Georgens
# ---------------------------------------------------------------------------

import os
import pyglet
#pyglet.options['audio'] = ('directsound', 'silent')
pyglet.options['shadow_window'] = False
import os.path
import glob
import Sound
import Queue as q
import threading
import time


class PygletBackgroundWorkerCommand(object):
    def __init__(self, command, args=None):
        self.command = command
        self.args = args


class PygletBackgroundWorker(threading.Thread):
    # Own thread for the pyglet stuff. Because own event loop and some
    # other shit like blocking functions etc.
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.terminate = False
        self.queue = queue
        self.player = None

    def play_sound(self, sound, volume=1.0):
        self.player = pyglet.media.Player()
        self.player.queue(sound)
        self.player.volume = volume
        self.player.play()
        # i know EOS_PAUSE is the default value for eos_action
        # but pyglet fuck me if i don't set it explicit
        self.player.eos_action = self.player.EOS_PAUSE

    def run(self):
        while not self.terminate:
            # without a item in the event queue the 'queue.get()' function
            # will block. But we must call the pyglet event loop at the end.
            if self.queue.qsize() > 0:
                q_command = self.queue.get()
                if q_command.command is "Terminate":
                    self.terminate = True
                elif q_command.command is "Play":
                    self.play_sound(*q_command.args)
                elif q_command.command is "Volume":
                    self.volume = q_command.args
                self.queue.task_done()
            time.sleep(5)  # slow down buddy
            pyglet.clock.tick()


class SoundHandler(object):
    def __init__(self, path_sounds):
        self.sounds = dict()
        self.base_path = os.path.dirname(__file__)
        self.__load_sounds__(path_sounds)
        # todo max Queue size is nice but ... actually i don't handle the Exception
        self.out_q = q.Queue(maxsize=10)
        self.pyglet_thread = PygletBackgroundWorker(self.out_q)
        self.pyglet_thread.start()
        self.__volume = 1.0  # default volume allowed values from 0.0 to 1.0

    def __del__(self):
        # The terminate command hopefully kills the pyglet background thread
        # hopefully because destructors are bad especially in python.
        self.out_q.put(PygletBackgroundWorkerCommand("Terminate"))

    def get_volume(self):
        return self.__volume

    def set_volume(self, volume=1.0):
        if volume > 1.0:
            volume = 1.0
        self.__volume = volume

    def play_sound(self, sound_id):
        sound = self.__get_sound__(sound_id)
        if sound is None:
            return False
        else:
            self.out_q.put(PygletBackgroundWorkerCommand("Play", [sound, self.__volume]))
            return True

    def delete_sound(self, sound_id):
        if sound_id in self.sounds:
            del self.sounds[sound_id]
            return True
        else:
            return False

    def get_ids(self):
        return self.sounds.keys()

    def __get_sound__(self, sound_id):
        if sound_id in self.sounds:
            return self.sounds[sound_id].get_sound()
        else:
            return None

    def __load_sounds__(self, base_path):
        """Load sounds from a given directory use the filename without extension as ID."""
        if not os.path.isdir(base_path):
            print "Error in load_sounds: Path %s is not a directory" % base_path
            return None

        old_dir = os.getcwd()
        os.chdir(base_path)
        # todo pyglet can handle much more filetypes as wave. Implement all formats
        for sound_file in glob.glob("*.MP3"):
            sound_id = sound_file.split('.')[0]
            sound = pyglet.media.load(os.path.join(base_path, sound_file), streaming=True)
            self.sounds[sound_id] = Sound.Sound(sound_id=sound_id, sound=sound)
        os.chdir(old_dir)
