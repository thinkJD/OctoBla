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

# globals
soundhandler = None


class OctoBla_Sounds(restful.Resource):
    def get(self):
        return soundhandler.get_ids()

api.add_resource(OctoBla_Sounds, '/Sounds')

# api.add_resource(HelloWorld, '/<string:song_id>')

def main():
    global soundhandler
    soundhandler = sh.SoundHandler()
    # debug only accessible from localhost
    app.run(debug=True)
    # global accessible
    #app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
