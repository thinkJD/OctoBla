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

app = Flask(__name__)
api = restful.Api(app)

# Constants
VERSION = "0.1.0"

# Globals
soundhandler = None

# Resources
class OctoBlaGeneral(restful.Resource):
    def get(self):
        return "Version:{}".format(VERSION)


class OctoBlaSound(restful.Resource):
    def get(self):
        """Get all available sounds from the server."""
        if soundhandler.get_ids():
            return soundhandler.get_ids()
        else:
            abort('404', message='No Sounds found')

    def put(self):
        """Add and Sound."""
        pass

    def delete(self, sound_id):
        """Removes a Sound from the Server. Until the next Restart."""
        if soundhandler.delete_sound(sound_id):
            return '', 204
        else:
            abort('404', message="Sound {} not found.".format(sound_id))


class OctoBlaPlayer(restful.Resource):
    """Play one specific sound."""
    def put(self, sound_id):
        if soundhandler.play_sound(sound_id):
            return sound_id, 201
        else:
            abort('404', message='Sound {} not found'.format(sound_id))


# Resource Routing
api.add_resource(OctoBlaGeneral, "/")
api.add_resource(OctoBlaSound, '/sound/<string:sound_id>', '/sound')
api.add_resource(OctoBlaPlayer, '/play/<string:sound_id>')

if __name__ == "__main__":
    soundhandler = sh.SoundHandler()

    # only accessible from localhost
    app.run(debug=True)

    # global accessible with optional ip range filter
    #app.run(host='0.0.0.0')
