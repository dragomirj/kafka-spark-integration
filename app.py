# *****************************************************************************
#  Dragomir J. - FLASK APP W/ CORS & SocketIO
# *****************************************************************************
import os
from flask import Flask, render_template
from flask_cors import CORS
from threading import Lock
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# DJ - CONFIG FILE WITH PREDEFINED VARIABLES
load_dotenv() # Load dotenv vars
thread = None

# FLASK, CORS & SOCKETIO CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
CORS(app) # Cross-Origin Resource Sharing
socketio = SocketIO(app, async_mode=None)
thread_lock = Lock()

# Home route
@app.route('/')
def home():
    return render_template('index.html', async_mode=socketio.async_mode)

# Add background thread functionality here!
def background_thread():
    return False

# SOCKETIO - BROADCAST
@socketio.event
def broadcast_event(message):
    emit('emit', message, broadcast=True)

# SOCKETIO - CONNECTION
@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.getenv('FLASK_PORT'))