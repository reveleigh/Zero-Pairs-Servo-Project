from flask import Flask, render_template
from flask_socketio import SocketIO
from servo_routines import binary_clock, sweep, reset_servos  # Import your servo functions
import logging
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
socketio = SocketIO(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Placeholder variable for the active servo routine
active_routine = None
routine_thread = None
stop_flag = threading.Event()

@app.route('/')
def index():
    return render_template('index.html')

def run_routine(routine):
    if routine == 'binary_clock':
        binary_clock(stop_flag)
    elif routine == 'sweep':
        sweep(stop_flag)

@socketio.on('start_routine')
def handle_start_routine(routine_name):
    global active_routine, routine_thread, stop_flag
    stop_flag = threading.Event()  # Reset the stop flag for a new routine

    if routine_thread and routine_thread.is_alive():
        logging.debug(f"Routine {active_routine} is already running")
        return

    active_routine = routine_name
    routine_thread = threading.Thread(target=run_routine, args=(routine_name,))
    routine_thread.start()
    logging.debug(f"Started routine: {routine_name}")

@socketio.on('stop_routine')
def handle_stop_routine():
    global stop_flag
    stop_flag.set()
    time.sleep(1)
    reset_servos()
    logging.debug("Stopping routine")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)