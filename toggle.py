import serial
import os
import sys

if os.path.exists("/dev/rfcomm0"):
    blue_port = serial.Serial("/dev/rfcomm0")
    blue_port.write("toggle{0:0d}\n".format(int(sys.argv[1])))
