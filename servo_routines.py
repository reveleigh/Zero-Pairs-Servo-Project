from adafruit_servokit import ServoKit
import time
import datetime
import threading

kit = ServoKit(channels=16)

# Initialize Servos 
for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[i].angle = 0

#Servo order for when used as a number line
servo_order = [7,6,5,4,3,2,1,0,8,9,10,11,12,13,14,15]


def binary_clock(stop_flag):
    """Displays time in hours and minutes on servos, updating only when necessary.
    Uses internet time if available, otherwise falls back to system time."""

    last_hour = -1
    last_minute = -1

    # Define servo positions (place values) for hours and minutes
    servo_positions = {
        "hours": {8: 4, 4: 5, 2: 6, 1: 7},
        "minutes": {32: 10, 16: 11, 8: 12, 4: 13, 2: 14, 1: 15}
    }

    def set_servo_angles(value, time_unit):
        """Sets servo angles based on the given time value (hour or minute)."""
        for place_value, servo_index in servo_positions[time_unit].items():
            bit_value = (value // place_value) % 2
            angle = 180 if bit_value == 1 else 0
            kit.servo[servo_index].angle = angle

    while not stop_flag.is_set():
        try:
            has_internet = check_internet_connection()

            if has_internet:
                now = datetime.datetime.now()
            else:
                # Get time from system clock
                result = subprocess.run(['date', '+%Y %m %d %H %M'], capture_output=True, text=True)
                year, month, day, hour_24, minute = map(int, result.stdout.split())
                now = datetime.datetime(year=year, month=month, day=day,
                                        hour=hour_24, minute=minute)

            hour_12 = now.hour % 12

            # Check if either hour or minute has changed before updating servos
            if hour_12 != last_hour or now.minute != last_minute:
                print(f"Time: {hour_12:02}:{now.minute:02}")
                set_servo_angles(hour_12, "hours")
                set_servo_angles(now.minute, "minutes")

            last_hour = hour_12
            last_minute = now.minute
            time.sleep(1)

        except Exception as e:
            print(f"Error getting time: {e}")
            time.sleep(1)

def sweep(stop_flag):
    # Main loop
    while not stop_flag.is_set():
        for angle in (0, 180):  
            for i in range(16):
                if not stop_flag.is_set():
                    kit.servo[i].angle = angle
                    time.sleep(0.1)   

        print("Servos moved successfully to", angle, "degrees.")


def show_moon(i):
    kit.servo[servo_order[i]].angle = 180
    time.sleep(0.5)  # Adjust sleep duration as needed
    kit.servo[servo_order[i]].angle = 0

def bounce(stop_flag):
    while not stop_flag.is_set():
        threads = []  # List to keep track of threads
        for i in range(16):
            t = threading.Thread(target=show_moon, args=(i,))  # Create a thread
            threads.append(t)
            t.start()  # Start the thread
            time.sleep(0.1)

        # Wait for all threads to finish (optional)
        for t in threads:
            t.join()
        
        # Reset threads list
        threads = []

        # Reverse bounce (count backward)
        for i in range(15, -1, -1):  # Iterate from 15 down to 0
            t = threading.Thread(target=show_moon, args=(i,))
            threads.append(t)
            t.start()
            time.sleep(0.1)

        # Wait for all reverse threads to finish
        for t in threads:
            t.join()
                

# Add a function to reset the servos to their initial position
def reset_servos():
    for i in range(16):
        kit.servo[i].angle = 0  