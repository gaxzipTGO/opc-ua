from telnetlib import COM_PORT_OPTION
import serial

COM_PORT = 'eth0'
BAUD_RATES = 9600

ser = serial.Serial(COM_PORT, BAUD_RATES)

try :
    while True:
        choice = input()

        if choice == '1' :  
            content = ser.readlines() 
            print(content) 
            choice = input()
        else :
            break


finally :
    print ('server stoped')