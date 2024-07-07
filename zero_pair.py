from adafruit_servokit import ServoKit
import time
import datetime
import threading

kit = ServoKit(channels=16)

# Initialise Servos 
for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[i].angle = 0

servos = [[0,1,2,3,4,5,6,7],
          [8,9,10,11,12,13,14,15]]

count_speed = 0.3

def reset():
        for i in range(16):
            kit.servo[i].angle = 0

def zero_pair_first_num(num1):
                    
    #Display num1
    if num1 >= 0:
        for i in range (num1):
            kit.servo[servos[0][i]].angle = 180
            time.sleep(count_speed)
    else:
        for i in range (abs(num1)):
            kit.servo[servos[1][i]].angle = 180
            time.sleep(count_speed)

def zero_pair(num1, num2, operation):

    #(+) + (+) | + answer
    if (operation == "+" #Addition
        and num1 >= 0 #Num 1 positive
        and num2 >= 0 #Num 2 positive
        and num1 + num2 <= 8): #Total is less than 9
        diff = num1 + num2 - num1
        for i in range(diff):
            kit.servo[servos[0][num1 + i]].angle = 180
            time.sleep(count_speed)

    #(+) - (+) | + answer
    elif (operation == "-" #Subtraction
        and num1 >= 0 #Num1 positive
        and num2 >= 0 #Num2 positive
        and num1 >= num2):#Total positive
        diff = num1 - num2
        for i in range(num1-1, diff-1, -1):
            kit.servo[servos[0][i]].angle = 0
            time.sleep(count_speed)

    #(+) - (+) | - answer
    elif (operation == "-" #Subtraction
        and num1 >= 0 #Num1 positive
        and num2 >= 0 #Num2 positive
        and num2 > num1): #Total is negative
        space = 8 - num1
        diff = num2 - num1

        #If enough room for zero pairs
        if diff <= space: 
            print(num1 + diff)
            for i in range(diff):
                print(i+num1)
                kit.servo[servos[0][i+num1]].angle = 180
                kit.servo[servos[1][i+num1]].angle = 180
                time.sleep(count_speed)
            print("####")
            
            time.sleep(1)
            for i in range(num1+diff, -1 ,-1):
                kit.servo[servos[0][i-1]].angle = 0
                time.sleep(count_speed)
            print("####")

    # (+) + (-)
    elif (operation == "+" #Addition
        and num1 >= 0 #num1 1 positive
        and num2 < 0 #num 2 is negative
        and num1 - num2 >= 0):# Total is positive
        print("###")
        for i in range(abs(num2)):
            kit.servo[servos[1][i]].angle = 180 #display negative values
            time.sleep(count_speed)
        print("###")
        time.sleep(0.5)

        diff = num1 - abs(num2)
        if abs(num2) > num1:
            count = num1
        else:
            count = abs(num2)

        for i in range(count):
            kit.servo[servos[0][i]].angle = 0
            kit.servo[servos[1][i]].angle = 0

    # (+) - (-)
    elif(operation == "-" #Subtraction
        and num1 >= 0 #num1 is positive
        and num2 < 0 #num2 is negative
        and num1 - num2 >= 0): #Total is positive
        diff = abs(num1 - abs(num2))
        for i in range(num1, num1+abs(num2)):
            kit.servo[servos[0][i]].angle = 180
            kit.servo[servos[1][i]].angle = 180
            time.sleep(count_speed)
        time.sleep(1)
        print ("###")
        for i in range(num1+abs(num2)-1, num1-1, -1):
            kit.servo[servos[1][i]].angle = 0
            time.sleep(count_speed)

    # (-) - (-)
    elif(operation == "-" #Subtraction
        and num1 <= 0 #num1 is negative
        and num2 <= 0 #num2 is negative
        and num1 - num2 <= 0): #Total is negative
        num1 = abs(num1)
        num2 = abs(num2)
        diff = num1 - num2
        for i in range(num1-1,num1-num2-1,-1):
            print (i)
            kit.servo[servos[1][i]].angle = 0
            time.sleep(count_speed)
        time.sleep(1)

    #(-) - (-) | + answer
    elif (operation == "-" #Subtraction
        and num1 <= 0 #num1 is negative
        and num2 <= 0 #num2 is negative
        and num1 - num2 > 0): #Total is negative
        num1 = abs(num1)
        num2 = abs(num2)
        space = 8 - num1
        diff = num2 - num1

        #If enough room for zero pairs
        if diff <= space: 
            print(num1 + diff)
            for i in range(diff):
                print(i+num1)
                kit.servo[servos[0][i+num1]].angle = 180
                kit.servo[servos[1][i+num1]].angle = 180
                time.sleep(count_speed)
            print("####")
            
            time.sleep(1)
            for i in range(num1+diff, -1 ,-1):
                kit.servo[servos[1][i-1]].angle = 0
                time.sleep(count_speed)
            print("####")

    # (-) + (-)
    if (operation == "+" #Addition
        and num1 <= 0 #num 1 negative
        and num2 <= 0 #num 2 negative
        and abs(num1) + abs(num2) <= 8): #Total is less than 9
        num1 = abs(num1)
        num2 = abs(num2)
        diff = num1 + num2 - num1
        for i in range(diff):
            kit.servo[servos[1][num1 + i]].angle = 180
            time.sleep(count_speed)

    # (-) + (+)
    elif (operation == "+" #Addition
        and num1 <= 0 #num1 1 negative
        and num2 > 0 #num 2 is positive
        and num1 - num2 <= 0):# Total is negative
        print("###")
        for i in range(num2):
            kit.servo[servos[0][i]].angle = 180 #display positive values
            time.sleep(count_speed)
        print("###")
        time.sleep(0.5)

        diff = abs(num1) - num2
        if num2 > abs(num1):
            count = abs(num1)
        else:
            count = num2

        for i in range(count):
            kit.servo[servos[0][i]].angle = 0
            kit.servo[servos[1][i]].angle = 0

    # (-) - (+)
    elif (operation == "-" #subtraction
        and num1 <= 0 #num1 is negative
        and num2 > 0 #num 2 is positive
        and num1 - num2 <= 0):# Total is negative
        print("###")
        num1 = abs(num1)

        for i in range(num1, num1+num2):
            kit.servo[servos[0][i]].angle = 180 
            kit.servo[servos[1][i]].angle = 180 
            time.sleep(count_speed)
        print("###")
        time.sleep(1)

        diff = abs(num1) - num2

        for i in range(num1+num2-1, num1-1, -1):
            kit.servo[servos[0][i]].angle = 0
            time.sleep(count_speed)
        
    time.sleep(3)
    reset()


