# Unoffical Spotify Playback HTTP server (Less Compatible with Normal Unoffical Spotify Playback api version)

### Control your spicetify client via HTTP requests
project based on [Terminal Spotify](https://github.com/Om-Thorat/Term-Spotify)

## Requirements
- [Spicetify](https://spicetify.app/docs/getting-started)
- python 3.13
- [Unoffical Spotify Playback api (ck fork)](https://github.com/CrazyKitty357/spotify-playback-api-ck)

### Notes
if you are on an arch based version of linux I recommend making a virtual environment and activating it before opening the 2 python files.  
my normal command for doing this is `python -m venv venv/`

## How to use
1. Download [playbackapick.js](https://github.com/CrazyKitty357/spotify-playback-api-ck/blob/main/dist/playbackapick.js)
2. put the modified playbackapick.js in the spicetify `Extensions` folder which can be found via running `spicetify config-dir`, if it's not already there make one and put it in there.
3. apply the modified extension to your client by running `spicetify config extensions playbackapick.js` then `spicetify apply` this will restart your spotify.
4. install the python requirements via running `python -m pip -r requirements.txt` or `pip -r requirements.txt`
5. run `server.py` this will connect to the websocket that's now applied to your spotify client
6. run `api.py` this will make the http server and will connect to the server.py

## HTTP API calls
`http://localhost:5000` - shows all of the http API calls in a nice, formatted list in your browser.