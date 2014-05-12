Project OctoBla
===============
A platform independent SoundServer with RESTful API based on Python.
Tested under OSX and Windows 7

ToDo:
-----
* Add more formats
* Add Player control (Queue, Stop, Play)
* Add Mixer features (Balance, Background / FX Ratio, Volume)
* Add Background Music
* Read some books about RESTful API Design

API Description
---------------
### General Information
    /general

    GET    -> Retrieves the current API Version

### Sounds
    /sound
    /sound/<string:sound_id>

    GET    -> Retrieves a list of all loaded ids
    PUT    -> Add a new sound
    DELETE -> Deletes a sound from the server

### Player
    /play/<string:sound_id>
  
    POST   -> Plays a specific sound

### Volume
    /volume/<float:volume>

    GET    -> Retrieves the current volume
    PUT    -> Set Volume the new value effects the next played song
