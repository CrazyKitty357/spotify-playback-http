# Unoffical Spotify Playback HTTP Server

### Control your spicetify client via HTTP requests
project based on [Terminal Spotify](https://github.com/Om-Thorat/Term-Spotify)

## Requirements
- [Spicetify](https://spicetify.app/docs/getting-started)
- python 3.13
- [Unoffical Spotify Playback api](https://github.com/Om-Thorat/Spicetify-extension) *

### Notes
if you are on an arch based version of linux I recommend making a virtual environment and activating it before opening the 2 python files.  
my normal command for doing this is `python -m venv venv/`  

there is also a branch where it's less compatible with the currently released version *(as of 4/10/2025)* of the unoffical playbackapi but it adds more features like the ability to request songs or the ability to be able to get nowplaying data and a spotify auth token via the http api.

## How to use
1. Download the [playbackapi.js](https://github.com/Om-Thorat/Spicetify-extension/blob/main/dist/playbackapi.js) and replace all instances of `443` with `8443` (for sudo's sake)
2. put the modified playbackapi.js in the spicetify `Extensions` folder which can be found via running `spicetify config-dir`, if it's not already there make one and put it in there.
3. apply the modified extension to your client by running `spicetify config extensions playbackapi.js` then `spicetify apply` this will restart your spotify.
4. install the python requirements via running `python -m pip -r requirements.txt` or `pip -r requirements.txt`
5. run `server.py` this will connect to the websocket that's now applied to your spotify client
6. run `api.py` this will make the http server and will connect to the server.py

## HTTP API calls
GET - `http://localhost:5000/playpause` - toggles playing and pausing  
GET - `http://localhost:5000/next` - skips to the next track  
GET - `http://localhost:5000/back` - it's like pressing the previous song arrow  
GET - `http://localhost:5000/shuffle` - toggles shuffle  
GET - `http://localhost:5000/repeat` - toggles looping between the 3 different states  
GET - `http://localhost:5000/data` - prints the current track title in the server.py