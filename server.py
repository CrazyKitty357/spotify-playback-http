from flask import Flask
from flask_socketio import SocketIO
import os
import time

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins='*')

player_data = {"track": "No track info yet"}
current_track_title = "No track info yet"

def get_spotify_data():
    """
    This function now returns the stored player data.
    """
    global player_data
    return player_data


@sio.on('command')
def handle_plugin_command(data):
    global player_data
    print("Received command from plugin:", data)
    if isinstance(data, str):
        current_track_title = data
        player_data = {"track": current_track_title}
    else:
        player_data = data 
    print("Updated player_data:", player_data)


@sio.on('request')
def handle_request(song_url):
    print("Request received for song URL:", song_url)
    sio.emit("input", "request " + song_url)

@sio.on('PlayPause')
def handle_playpause():
    print("PlayPause command received")
    sio.emit("input", "PlayPause")

@sio.on('Next')
def handle_next():
    print("Next command received")
    sio.emit("input", "Next")

@sio.on('Prev')
def handle_prev():
    print("Prev command received")
    sio.emit("input", "Prev")

@sio.on('Shuffle')
def handle_shuffle():
    print("Shuffle command received")
    sio.emit("input", "Shuffle")

@sio.on('Repeat')
def handle_repeat():
    print("Repeat command received")
    sio.emit("input", "Repeat")

@sio.on('getdata')
def handle_getdata():
    print("getdata command received")
    data_to_send = get_spotify_data()
    sio.emit('player_data', data_to_send)

if __name__ == "__main__":
    sio.run(app, host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 8443)), debug=False)