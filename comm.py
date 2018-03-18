import serial
import os

while True:
    if os.path.exists("/dev/rfcomm0"):
        blue_port = serial.Serial("/dev/rfcomm0")
        blue_port.write("CONNECT\n")
        data = blue_port.readline()
        if data == "OK\n":
            print "OK"
        break
