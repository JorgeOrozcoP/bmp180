#!/usr/bin/env python3

"""
based on ButtonLED by freenove
Use to test that button connections work.
"""
import RPi.GPIO as GPIO

buttonPin = 12    # define buttonPin


def setup():
    GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
    # set buttonPin to PULL UP INPUT mode
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop():
    while True:
        # if button is pressed
        if GPIO.input(buttonPin) == GPIO.LOW:
            print('led turned on >>>')
        else:
            print('led turned off <<<')


def destroy():
    GPIO.cleanup()  # Release GPIO resource


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
