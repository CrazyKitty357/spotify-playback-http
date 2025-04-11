from flask import Flask, request, jsonify
import socketio
import requests
import base64
import urllib.parse
import json

app = Flask(__name__)
sio_client = socketio.Client()

SERVER_ADDRESS = 'http://127.0.0.1:8443'  # Address of server.py
with open("auth.json") as f:
    data = json.load(f)[0]


CLIENT_ID = data["client_id"]
CLIENT_SECRET = data["client_secret"]
SPOTIFY_ACCESS_TOKEN = data["auth_token"]
REDIRECT_URI = "http://localhost:5000/callback"


class Player:
    def __init__(self):
        self.connected = False
        self.player_data = {}
        self.connect_to_server()

    def connect_to_server(self):
        try:
            sio_client.connect(SERVER_ADDRESS)
            self.connected = True
            print("SocketIO client connected to server.py")

        except socketio.exceptions.ConnectionError as e:
            print(f"Error connecting to server.py: {e}")
            self.connected = False

    def send_command(self, command, data=None):
        if self.connected:
            if data:
                sio_client.emit(command, data)
            else:
                sio_client.emit(command)
        else:
            print("Not connected to server.py. Cannot send command.")

    def toggleplay(self):
        self.send_command("PlayPause")

    def next(self):
        self.send_command("Next")

    def back(self):
        self.send_command("Prev")

    def shuffle(self):
        self.send_command("Shuffle")

    def repeat(self):
        self.send_command("Repeat")

    def getdata(self):
        self.send_command("getdata")

    def request_song(self, song_url):
        self.send_command("request", song_url)


pl = Player()

@app.route('/')
def home():
    return "Spicetify Player API is running!<br>/playpause - Plays and pauses the current track<br>/next - skips the current song<br>/back - presses the back arrow<br>/shuffle - toggles shuffle<br>/repeat - toggles between the 3 loop states (not looping) (looping playlist) (looping current song)<br>/data - sends data to the server (does nothing when called via the http api)<br>/request - sends a song directly to spotify's built-in queue system. Can be used like <a href='request?song=https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8'>/request?song=https://spotify.com/song_url</a><br>/auth - calls back with a spotify user token | <b>MUST HAVE A VALID SPOTIFY CLIENT ID AND SECRET TO USE</b><br>/settoken - sets your spotify user api token. Can be used like <a href='settoken?token=api_token'>/settoken?token=api_token</a><br>/nowplaying - responds with a mirror of spotify's now playing from their api | <b>MUST HAVE A SPOTIFY USER TOKEN TO USE</b>"

@app.route('/playpause', methods=['GET'])
def playpause():
    pl.toggleplay()
    return jsonify({"status": "success", "action": "playpause"})

@app.route('/next', methods=['GET'])
def next_track():
    pl.next()
    return jsonify({"status": "success", "action": "next"})

@app.route('/back', methods=['GET'])
def back_track():
    pl.back()
    return jsonify({"status": "success", "action": "back"})

@app.route('/shuffle', methods=['GET'])
def shuffle_tracks():
    pl.shuffle()
    return jsonify({"status": "success", "action": "shuffle"})

@app.route('/repeat', methods=['GET'])
def repeat_tracks():
    pl.repeat()
    return jsonify({"status": "success", "action": "repeat"})

@app.route('/data', methods=['GET'])
def get_player_data():
    pl.getdata()
    return jsonify({"status": "success", "action": "getdata", "message": "Check server.py logs for data, data is not directly returned via socket in this setup."})

@app.route('/request', methods=['GET'])
def request_song_route():
    song_url = request.args.get('song')
    if not song_url:
        return jsonify({"status": "error", "message": "Missing song URL in request"}), 400
    pl.request_song(song_url)
    return jsonify({"status": "success", "action": "request", "song_url": song_url})

@app.route('/nowplaying', methods=['GET'])
def now_playing():
    headers = {
        "Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"
    }
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if r.status_code == 204:
        return jsonify({"status": "success", "message": "Nothing currently playing"})

    if r.status_code != 200:
        return jsonify({"status": "error", "message": "Failed to fetch now playing", "details": r.json()})

    return jsonify({"status": "success", "now_playing": r.json()})

@app.route('/auth')
def auth():
    scopes = "user-read-playback-state"
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scopes
    }
    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return f'<a href="{url}">Authorize Spotify</a>'


@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed D:"

    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post(token_url, data=data, headers=headers)
    if r.status_code != 200:
        return f"Failed to get token: {r.text}"

    token_info = r.json()
    global SPOTIFY_ACCESS_TOKEN
    SPOTIFY_ACCESS_TOKEN = token_info["access_token"]

    return jsonify({"status": "success", "token": SPOTIFY_ACCESS_TOKEN})

@app.route('/settoken')
def set_token():
    token = request.args.get('token')
    if not token:
        return jsonify({"status": "error", "message": "Missing token parameter"}), 400

    try:
        with open("auth.json", "r") as f:
            auth_data = json.load(f)
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "auth.json file not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Error decoding auth.json"}), 500

    if auth_data and isinstance(auth_data, list) and auth_data[0]:
        auth_data[0]["auth_token"] = token
    else:
        return jsonify({"status": "error", "message": "Invalid auth.json structure"}), 500

    try:
        with open("auth.json", "w") as f:
            json.dump(auth_data, f, indent=4)
    except IOError:
        return jsonify({"status": "error", "message": "Error writing to auth.json"}), 500

    global SPOTIFY_ACCESS_TOKEN
    SPOTIFY_ACCESS_TOKEN = token

    return jsonify({"status": "success", "message": "Token updated successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)