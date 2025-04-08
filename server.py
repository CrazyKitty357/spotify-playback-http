from flask import Flask
from flask_socketio import SocketIO
import os

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins='*')

@sio.on('message')
def handle_message(data):
    print("Message received:", data)

@sio.on('command')
def handle_command(data):
    print("Command received:", data)
    sio.emit("input", data)

if __name__ == "__main__":
    sio.run(app, host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 8443)), debug=False)