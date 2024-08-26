from flask import Flask, render_template, request, jsonify
from servo_routines import binary_clock, sweep, reset_servos, bounce
from zero_pair import zero_pair, zero_pair_first_num 
import traceback

import logging
import threading
import time

app = Flask(__name__, static_folder='/home/russell/env/static', template_folder='/home/russell/templates')
app.config['SECRET_KEY'] = '123456'  # Replace with your actual secret key

# Set up logging (optional)
logging.basicConfig(level=logging.DEBUG)

active_routine = None
routine_thread = None
stop_flag = threading.Event()

@app.route('/')
def index():
    return render_template('index.html')

# Add status endpoint
@app.route('/status')
def get_status():
    global active_routine
    if active_routine:
        return 'running'
    else:
        return 'idle'

def run_routine(routine):
    global stop_flag
    stop_flag.clear()
    if routine == 'binary_clock':
        binary_clock(stop_flag)
    elif routine == 'sweep':
        sweep(stop_flag)
    elif routine == 'bounce':
        bounce(stop_flag)

@app.route('/start_binary_clock')
def start_binary_clock():
    global active_routine, routine_thread
    
    # If a routine is already running, stop it
    if routine_thread and routine_thread.is_alive():
        stop_flag.set()
        routine_thread.join()  # Wait for the old routine to finish gracefully

    active_routine = 'binary_clock'
    routine_thread = threading.Thread(target=run_routine, args=('binary_clock',))
    routine_thread.start()
    logging.debug("Started binary_clock routine")
    return "running"


@app.route('/start_sweep')
def start_sweep():
    global active_routine, routine_thread
    
    # If a routine is already running, stop it
    if routine_thread and routine_thread.is_alive():
        stop_flag.set()
        routine_thread.join()

    active_routine = 'sweep'
    routine_thread = threading.Thread(target=run_routine, args=('sweep',))
    routine_thread.start()
    logging.debug("Started sweep routine")
    return "running"

@app.route('/start_bounce')
def start_bounce():
    global active_routine, routine_thread
    
    # If a routine is already running, stop it
    if routine_thread and routine_thread.is_alive():
        stop_flag.set()
        routine_thread.join()

    active_routine = 'bounce'
    routine_thread = threading.Thread(target=run_routine, args=('bounce',))
    routine_thread.start()
    logging.debug("Started bounce routine")
    return "running"


@app.route('/stop_routine')
def stop_routine():
    global stop_flag
    stop_flag.set()
    time.sleep(1) 
    reset_servos()
    logging.debug("Stopping routine")
    return "idle"

logging.basicConfig(level=logging.DEBUG)

@app.route('/zero-pair', methods=['GET'])
def zero_pair_route():
    if request.method == 'GET':
        try:
            num1 = request.args.get('num1')
            num2 = request.args.get('num2')
            operation = request.args.get('operation')
            logging.debug(f"Received: num1={num1}, num2={num2}, operation={operation}")

            if num1 and not num2 and not operation:  # Only num1 provided
                num1 = int(num1)
                servo_angles_num1 = zero_pair_first_num(num1)
                return jsonify(servo_angles_num1=servo_angles_num1)
            elif num1 and num2 and operation:  # All parameters provided
                num1 = int(num1)
                num2 = int(num2)
                logging.debug("Calling zero_pair function")
                result = zero_pair(num1, num2, operation)
                logging.debug(f"Result: {result}")
                return jsonify(result=result)
            else:  # Initial page load or invalid input
                return render_template('zero-pair.html')
        except ValueError as e:
            logging.error(f"ValueError: {e}")
            return jsonify(error=str(e)), 400
        except Exception as e:
            logging.error(f"Exception: {e}")
            traceback.print_exc()
            return jsonify(error=str(e)), 500

@app.route('/set_time', methods=['GET', 'POST'])
def set_time():
    if request.method == 'POST':
        hour = request.form.get('hour')
        minute = request.form.get('minute')

        if hour and minute:
            try:
                # Validate the input (ensure hour is 1-12, minute is 0-59)
                hour = int(hour)
                minute = int(minute)
                if 1 <= hour <= 12 and 0 <= minute <= 59:
                    # Convert 12-hour format to 24-hour format for system setting
                    hour_24 = hour % 12  # 12 becomes 0 (midnight), rest remain the same
                    subprocess.call(['sudo', 'date', '+%H:%M', '-s', f'{hour_24:02d}:{minute:02d}'])
                    return render_template('set_time.html', message='Time set successfully! (Temporary, no RTC)')
                else:
                    return render_template('set_time.html', message='Invalid time format. Hour should be 1-12, minute should be 0-59.')
            except ValueError:
                return render_template('set_time.html', message='Invalid time format. Please provide integers for hour and minute.')
        else:
            return render_template('set_time.html', message='Missing hour or minute parameters.')
    else:  # GET request
        return render_template('set_time.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
