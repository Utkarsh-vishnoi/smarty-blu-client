from threading import Thread
import subprocess
import RPi.GPIO as PIN
import Adafruit_CharLCD
from time import sleep

# LCD
# RS = 9
# RW -> GROUND
# EN = 10
# D4 = 11
# D5 = 12
# D6 = 13
# D7 = 14
lcd = Adafruit_CharLCD.Adafruit_CharLCD(9, 10, 11, 12, 13, 14, 16, 2, 27)

degree_symbol = bytearray([0xe, 0xa, 0xe, 0x0, 0x0, 0x0, 0x0, 0x0])
lcd.create_char(0, degree_symbol)
lcd.clear()

PIN.setmode(PIN.BCM)

# Buttons
PIN.setup(4, PIN.IN, pull_up_down=PIN.PUD_DOWN)
PIN.setup(5, PIN.IN, pull_up_down=PIN.PUD_DOWN)
PIN.setup(6, PIN.IN, pull_up_down=PIN.PUD_DOWN)


def lcd_set(data):
    lcd.clear()
    lcd.home()
    lcd.message(data)


def check_bluetooth_state():
    p = subprocess.Popen(["sudo", "python", "/home/utkarsh/Desktop/blu-client/comm.py"], stdout=subprocess.PIPE)
    result, error = p.communicate()
    if result == "OK\n":
        return True
    else:
        return False


def lights():
    prev_a = 0
    prev_b = 0
    prev_c = 0
    try:
        while True:
            a = PIN.input(4)
            b = PIN.input(5)
            c = PIN.input(6)
            if (not prev_a) and a:
                subprocess.Popen(["sudo", "python", "/home/utkarsh/Desktop/blu-client/toggle.py", "2"],
                                 stdout=subprocess.PIPE)
            if (not prev_b) and b:
                subprocess.Popen(["sudo", "python", "/home/utkarsh/Desktop/blu-client/toggle.py", "3"],
                                 stdout=subprocess.PIPE)
            if (not prev_c) and c:
                subprocess.Popen(["sudo", "python", "/home/utkarsh/Desktop/blu-client/toggle.py", "4"],
                                 stdout=subprocess.PIPE)
            prev_a = a
            prev_b = b
            prev_c = c
            sleep(0.05)
    except (KeyboardInterrupt, SystemExit):
        PIN.cleanup()


def dht():
    p = subprocess.Popen(["sudo", "python", "/home/utkarsh/Desktop/blu-client/dht.py", ],
                         stdout=subprocess.PIPE)
    result, error = p.communicate()
    print result


def initiate_core_events():
    lights_thread = Thread(target=lights)
    lights_thread.start()
    dht_thread = Thread(target=dht)
    dht_thread.start()


def bluetooth():
    lcd_set("Connecting to\nRemote PI")
    print "Connecting to Remote PI"
    subprocess.Popen(["sudo", "rfcomm", "connect", "hci0", "B8:27:EB:65:BC:20"], stdout=subprocess.PIPE)
    sleep(5)
    if check_bluetooth_state():
        lcd_set("Connected to\nRemote PI")
        print "Connected to Remote PI"
        initiate_core_events()
    else:
        lcd_set("Error connecting\nto remote PI")
        print "Error connecting to PI"


def main():
    bluetooth_thread = Thread(target=bluetooth)
    bluetooth_thread.start()

    while True:
        sleep(1)


if __name__ == "__main__":
    main()
