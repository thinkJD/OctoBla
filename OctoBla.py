# ---------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jd.georgens@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return.
#                                                        Jan-Daniel Georgens
# ---------------------------------------------------------------------------

from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, abort
import SoundHandler as sh
import ConfigParser as conf
import os

app = Flask(__name__)
api = restful.Api(app)

# Constants
VERSION = "0.1.0"

# Globals
soundhandler = None

# Resources
class OctoBlaGeneral(restful.Resource):
    def get(self):
        return "Version:{}".format(VERSION), 200  # ok


class OctoBlaSound(restful.Resource):
    def get(self):
        """Get all available sounds from the server."""
        if soundhandler.get_ids():
            return soundhandler.get_ids(), 200
        else:
            abort('404', message='No Sounds found')

    def put(self):
        """Add and Sound."""
        return 501  # not implemented

    def delete(self, sound_id):
        """Removes a Sound from the Server. Until the next Restart."""
        if soundhandler.delete_sound(sound_id):
            return '', 204  # No Content
        else:
            abort('404', message="Sound {} not found.".format(sound_id))


class OctoBlaVolume(restful.Resource):
    def get(self):
        return soundhandler.get_volume(), 200

    def put(self, volume):
        soundhandler.set_volume(volume)
        return volume, 202


class OctoBlaPlayer(restful.Resource):
    """Play one specific sound."""
    def put(self, sound_id):
        if soundhandler.play_sound(sound_id):
            return sound_id, 202
        else:
            abort('404', message='Sound {} not found'.format(sound_id))


# Resource Routing
api.add_resource(OctoBlaGeneral, "/")
api.add_resource(OctoBlaSound, '/sound/<string:sound_id>', '/sound')
api.add_resource(OctoBlaPlayer, '/play/<string:sound_id>')
api.add_resource(OctoBlaVolume, '/volume/<float:volume>', "/volume")

if __name__ == "__main__":
    # read configuration, configure environment
    base_path =os.path.dirname(__file__)
    config_path = os.path.join(base_path, 'settings.cfg')
    config = conf.ConfigParser()
    config.read(config_path)

    soundhandler = sh.SoundHandler(os.path.join(base_path, config.get('Paths', 'SoundDir')))
    soundhandler.set_volume(config.get('Audio', 'DefaultVolume'))

    # only accessible from localhost.
    # Don't use in productive environment!
    app.run(debug=True)

    # global accessible with optional ip range filter
    #app.run(host=config.get('General', 'Host'), port=config.get('General', 'Port'))
