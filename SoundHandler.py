# ---------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jd.georgens@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return.
#                                                        Jan-Daniel Georgens
# ---------------------------------------------------------------------------

import pyglet
pyglet .options['shadow_window'] = False
import os
import os.path
import glob
import Sound


class SoundHandler(object):
    def __init__(self):
        #self.player = pyglet.media.Player()
        self.sounds = dict()
        self.base_path = os.path.dirname(__file__)
        self.load_sounds(os.path.join(self.base_path, "Sounds"))

    def queue_sound(self, sound_id):
        pass

    def play(self):
        self.player.play()

    def stop_playback(self):
        pass

    def play_sound(self, sound_id):
        pass

    def get_ids(self):
        return self.sounds.keys()

    def load_sounds(self, base_path):
        """Load sounds from a given directory use the filename without extension as ID."""
        if not os.path.isdir(base_path):
            print "Error in load_sounds: Path %s is not a directory" % base_path
            return None

        old_dir = os.getcwd()
        os.chdir(base_path)
        #todo pyglet can handle much mord filetypes as wave. Implement all formats
        print "Load Sounds:"
        for sound_file in glob.glob("*.wav"):
            sound_id = sound_file.split('.')[0]
            print "Loading: %s" % os.path.join(base_path, sound_file)
            sound = pyglet.media.load(os.path.join(base_path, sound_file), streaming=False)
            self.sounds[sound_id] = Sound.Sound(sound_id=sound_id, sound=sound)
        os.chdir(old_dir)

