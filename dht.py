import Adafruit_CharLCD
import serial

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

rfcomm = serial.Serial("/dev/rfcomm0")


def lcd_set(data):
    lcd.clear()
    lcd.home()
    lcd.message(data)


def main():
    while True:
        data = rfcomm.readline()
        formatted_data = data.split("||")
        if formatted_data[0] == "dht":
            temperature = formatted_data[1]
            humidity = formatted_data[2].replace("\n", "")
            lcd_set("Temp = {0}\x00C\nHumidity = {1}% ".format(temperature, humidity))


if __name__ == "__main__":
    main()
