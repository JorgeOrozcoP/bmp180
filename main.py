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
from db.bmp180_db import bmp180_sqlite3

from time import sleep
# from datetime import datetime
import RPi.GPIO as GPIO


def loop(mcp, lcd, buttonPin, db):

    mcp.output(3, 0)     # turn on LCD backlight
    lcd.begin(16, 2)     # set number of LCD lines and columns

    sleeping_period = 0.5  # seconds
    light_max_time = 5  # seconds
    period_until_db_write = 10 # 60 * 30 # seconds
    read_data_period = 1  # seconds

    pressed_button = False
    main_timer = 0
    light_timer = 0


    # time conversion
    light_max_time = light_max_time / sleeping_period
    period_until_db_write = period_until_db_write / sleeping_period
    read_data_period = read_data_period / sleeping_period


    while(True):

        if main_timer % read_data_period == 0:
            temp, press, alt = readBmp180()

            lcd.setCursor(0, 0)  # set cursor position
            lcd.message("Temp: " + str(temp) + " C\n")  # display temp
            lcd.message("Press: " + str(press))   # display pressure

        if GPIO.input(buttonPin) == GPIO.LOW and not pressed_button:
            pressed_button = True
            mcp.output(3, 1)

        if pressed_button:
            light_timer += 1
            if light_timer >= light_max_time:
                mcp.output(3, 0)
                pressed_button = False
                light_timer = 0


        if main_timer % period_until_db_write == 0:
            db.insert(temp, press)

        main_timer += 1
        sleep(sleeping_period)


def destroy(mcp, lcd, db):
    lcd.clear()
    mcp.output(3,0)
    GPIO.cleanup()
    db.close_db()


def setup(buttonPin=12):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    # Create PCF8574 GPIO adapter.

    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except OSError:
        print("I2C Address Error!")
        exit(1)


    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)

    # create database instance
    db = bmp180_sqlite3(device="raspberrypizero")

    return mcp, lcd, db


if __name__ == '__main__':
    print('Program running ... ')

    buttonPin = 12
    mcp, lcd, db = setup(buttonPin)

    try:
        loop(mcp, lcd, buttonPin, db)
    except KeyboardInterrupt:
        destroy(mcp, lcd, db)
