from adafruit_servokit import ServoKit
import time
import datetime
import threading

kit = ServoKit(channels=16)

servo_order = [7,6,5,4,3,2,1,0,8,9,10,11,12,13,14,15]

# Initialize Servos 
for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[i].angle = 0


def show_moon(i):
    kit.servo[servo_order[i]].angle = 180
    time.sleep(0.5)  # Adjust sleep duration as needed
    kit.servo[servo_order[i]].angle = 0

def bounce():
    threads = []  # List to keep track of threads
    for i in range(16):
        t = threading.Thread(target=show_moon, args=(i,))  # Create a thread
        threads.append(t)
        t.start()  # Start the thread
        time.sleep(0.1)

    # Wait for all threads to finish (optional)
    for t in threads:
        t.join()
while True:
    show_moon(1)
    show_moon(13)
    show_moon(7)
    show_moon(10)
    show_moon(3)
    show_moon(15)

