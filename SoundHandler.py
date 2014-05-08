# ---------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jd.georgens@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return.
#                                                        Jan-Daniel Georgens
# ---------------------------------------------------------------------------

import os
import pyglet
pyglet.options['shadow_window'] = False
import os.path
import glob
import Sound


class SoundHandler(object):
    def __init__(self):
        self.sounds = dict()
        self.base_path = os.path.dirname(__file__)
        self.__load_sounds__(os.path.join(self.base_path, "Sounds"))

    def __get_sound__(self, sound_id):
        return self.sounds[sound_id].get_sound()

    def play(self):
        if not self.sound_queue:
            return

        player = pyglet.media.Player()
        for sound in self.sound_queue:
            player.queue(sound)
        player.play()
        self.__wait_for_player__(player)

    def __wait_for_player__(self, player):
        while player.playing:
            pyglet.clock.tick()

    def play_sound(self, sound_id):
        sound = self.__get_sound__(sound_id)

        player = pyglet.media.Player()
        player.queue(sound)
        player.play()
        player.eos_action = player.EOS_PAUSE
        self.__wait_for_player__(player)

    def get_ids(self):
        return self.sounds.keys()

    def __load_sounds__(self, base_path):
        """Load sounds from a given directory use the filename without extension as ID."""
        if not os.path.isdir(base_path):
            print "Error in load_sounds: Path %s is not a directory" % base_path
            return None

        old_dir = os.getcwd()
        os.chdir(base_path)
        # todo pyglet can handle much more filetypes as wave. Implement all formats
        for sound_file in glob.glob("*.wav"):
            sound_id = sound_file.split('.')[0]
            sound = pyglet.media.load(os.path.join(base_path, sound_file), streaming=False)
            self.sounds[sound_id] = Sound.Sound(sound_id=sound_id, sound=sound)
        os.chdir(old_dir)
