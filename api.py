from flask import Flask, request, jsonify
import socketio

app = Flask(__name__)
sio_client = socketio.Client()

SERVER_ADDRESS = 'http://127.0.0.1:8443'  # Address of server.py

class Player:
    def __init__(self):
        self.connected = False
        self.connect_to_server()

    def connect_to_server(self):
        try:
            sio_client.connect(SERVER_ADDRESS)
            self.connected = True
            print("SocketIO client connected to server.py")
        except socketio.exceptions.ConnectionError as e:
            print(f"Error connecting to server.py: {e}")
            self.connected = False

    def send_command(self, command):
        if self.connected:
            sio_client.emit('command', command)
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


pl = Player()

@app.route('/')
def home():
    return "Spicetify Player API is running!"

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
    return jsonify({"status": "success", "action": "getdata", "message": "Data request sent to server.py. Check server.py logs for response."}) # Data will be printed in server.py logs

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)