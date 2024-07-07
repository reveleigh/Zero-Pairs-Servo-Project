import time

number_line = [1, 2, 3, 4, 5, 6, 7, 8, 0, -1, -2, -3, -4, -5, -6, -7, -8]

num1 = int(input("Enter the first number: "))
                
#Display num1
if num1 >= 0:
    for i in range (num1):
        print (number_line[i])
else:
    for i in range (abs(num1)):
        print (number_line[i+9])

operation = input("Enter sign: + or -")

num2 = int(input("Enter the second number: "))


#(+) + (+) | + answer
if (operation == "+" #Addition
    and num1 >= 0 #Num 1 positive
    and num2 >= 0 #Num 2 positive
    and num1 + num2 <= 8): #Total is less than 9
    diff = num1 + num2 - num1
    for i in range(diff):
        print (num1 + i + 1)

#(+) - (+) | + answer
elif (operation == "-" #Subtraction
      and num1 >= 0 #Num1 positive
      and num2 >= 0 #Num2 positive
      and num1 >= num2):#Total positive
    diff = num1 - num2
    for i in range(num1, diff, -1):
        print (i)

#(+) - (+) | - answer
elif (operation == "-" #Subtraction
      and num1 >= 0 #Num1 positive
      and num2 >= 0 #Num2 positive
      and num2 > num1): #Total is negative
    diff = num2 - num1

    #If enough room for zero pairs
    if num1 + num2  <= 8:
        print(num1 + diff)
        for i in range(num1 + diff + 8, num1 + 8, -1):
            print (number_line[i])
        print("####")
        
        time.sleep(1)
        for i in range(num1+diff, 0 ,-1):
            print(i)
        print("####")
        time.sleep(2)
        for i in range(num1, 0, -1):
            print(number_line[i + diff + 8], " off")
            print(number_line[i + 8], " on")
            time.sleep(0.5)

    #If not enough room for zero pairs
    else:
        for i in range(num1, 0, -1):
            print(number_line[i-1])
        print ("###")
        time.sleep(0.5)
        for i in range(diff):
            print(number_line[i]," on")
            print(number_line[i+9], " on")
        print("###")
        time.sleep(0.5)
        for i in range(diff, 0, -1):
            print(number_line[i-1], " off")
            
# (+) + (-)
elif (operation == "+" #Addition
      and num1 >= 0 #num1 1 positive
      and num2 < 0 #num 2 is negative
      and num1 - num2 >= 0):# Total is positive
    for i in range(num1):
        print(number_line[i])
    print("###")
    time.sleep(0.5)
    for i in range(abs(num2)):
        print(number_line[i+9]) #display negative values
    print("###")
    time.sleep(0.5)

    diff = num1 - abs(num2)
    for i in range(num1 - diff):
        print(number_line[i], " off")
        print(number_line[i+9], " off")
    print("###")
    time.sleep(0.5)
    shift = num1 - diff
    for i in range(shift):
        print (number_line[num1 - i - 1], " off")
        print (number_line[num1 - diff - i - 1], " on")

# (+) - (-)
elif(operation == "-" #Subtraction
     and num1 >= 0 #num1 is positive
     and num2 < 0 #num2 is negative
     and num1 - num2 >= 0): #Total is positive
    for i in range(num1):
        print(number_line[i])
    print ("###")
    time.sleep(1)
    diff = num1 - abs(num2)
    for i in range(num1, num1+diff):
        print(number_line[i])
        print(number_line[i+9])
    print ("###")
    time.sleep(1)
    for i in range(num1+diff,num1,-1):
        print(number_line[i+8], "off")

    

      

#If first number pos and subtracting total <0


#If first number neg and subtracting total to 

#If first number neg and adding total<1

#If first number neg and adding total > 0

        


