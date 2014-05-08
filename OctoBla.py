# ---------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jd.georgens@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return.
#                                                        Jan-Daniel Georgens
# ---------------------------------------------------------------------------

from flask import Flask
from flask.ext import restful
import SoundHandler as sh

app = Flask(__name__)
api = restful.Api(app)

# constants
VERSION = "0.0.1"

# globals
soundhandler = None

class OctoBlaGeneral(restful.Resource):
    def get(self):
        return VERSION


class OctoBlaSound(restful.Resource):
    def get(self):
        """Get all available sounds from the server."""
        return soundhandler.get_ids()

    def put(self):
        """Add and Sound."""
        pass

    def delete(self, sound_id):
        """Delete a sound from the Server"""
        return '', 204
        pass


class OctoBlaPlayer(restful.Resource):
    """Play one specific sound."""
    def put(self, sound_id):
        soundhandler.play_sound(sound_id)
        return "Done!", 201


def main():
    global soundhandler
    soundhandler = sh.SoundHandler()

    # Resource Routing
    api.add_resource(OctoBlaGeneral, "/general")
    api.add_resource(OctoBlaSound, '/sound/<string:sound_id>')
    api.add_resource(OctoBlaPlayer, '/player/<string:sound_id>')

    # debug. only accessible from localhost
    app.run(debug=True)
    # global accessible with optional ip range filter
    #app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
