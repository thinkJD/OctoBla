Project OctoBla
===============
A platform independent SoundServer with REST API based on Python.


API Description
-------------------
* /general
    > GET    -> Retrieves the current API Version
* /sound/<string:sound_id>
    > GET    -> Retrieves a list of all loaded ids
    > PUT
    > DELETE -> Delets a sound from the server
* /player/<string:sound_id>
    > GET    -> Retrieves the current playing song
    > POST   -> Plays a specific sound
