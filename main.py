#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from lcd1602.PCF8574 import PCF8574_GPIO
from lcd1602.Adafruit_LCD1602 import Adafruit_CharLCD
from bmp180.bmp180_2 import readBmp180

from time import sleep
# from datetime import datetime
import RPi.GPIO as GPIO


def loop(mcp, lcd, buttonPin):

    mcp.output(3, 0)     # turn on LCD backlight
    lcd.begin(16, 2)     # set number of LCD lines and columns

    pressed_button = False
    main_timer = 0
    light_timer = 0
    light_max_time = 10

    while(True):

        if main_timer % 2 == 0:
            temp, press, alt = readBmp180()
            # lcd.clear()
            lcd.setCursor(0, 0)  # set cursor position
            lcd.message("Temp: " + str(temp) + " C\n")  # display temp
            lcd.message("Press: " + str(press))   # display pressure

        if GPIO.input(buttonPin) == GPIO.LOW and not pressed_button:
            pressed_button = True
            mcp.output(3, 1)
            print("Turning light on.")

        if pressed_button:
            light_timer += 1
            if light_timer >= light_max_time:
                mcp.output(3, 0)
                pressed_button = False
                light_timer = 0

        main_timer += 1
        if main_timer % 2 == 0:
            main_timer = 0

        sleep(0.5)


def destroy(mcp, lcd):
    lcd.clear()
    mcp.output(3,0)
    GPIO.cleanup()


def setup(buttonPin=12):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    # Create PCF8574 GPIO adapter.
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print('I2C Address Error !')
            exit(1)

    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)

    return mcp, lcd, buttonPin


if __name__ == '__main__':
    print('Program running ... ')

    mcp, lcd, buttonPin = setup(buttonPin=12)

    try:
        loop(mcp, lcd, buttonPin)
    except KeyboardInterrupt:
        destroy(mcp, lcd)
