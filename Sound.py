# ---------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jd.georgens@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return.
#                                                        Jan-Daniel Georgens
# ---------------------------------------------------------------------------


class Sound(object):
    """Data class for a single Sound."""
    def __init__(self, sound_id, sound):
        self.__sound_id = sound_id
        self.__sound = sound

    def get_id(self):
        """Returns the ID of the sound. The ID is the internal reference."""
        return self.__sound_id

    def get_sound(self):
        """Returns the sounf (WAV file)."""
        return self.__sound