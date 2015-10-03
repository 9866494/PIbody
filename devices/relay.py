#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

class Relay:
    def __init__(self, pins):
        self.pins = []

        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 1)
            self.pins.append(p)

    def on(self, relay_number):
        print ('Relay %s at pin %s on' % (relay_number, self.pins[relay_number - 1]))
        GPIO.output(self.pins[relay_number - 1], 0)

    def off(self, relay_number):
        print ('Relay %s at pin %s off' % (relay_number, self.pins[relay_number - 1]))
        GPIO.output(self.pins[relay_number - 1], 1)

GPIO.setmode(GPIO.BOARD)

r = Relay([11, 12, 13, 15])

for i in range(10):
    r.on(1)
    sleep(.01)
    r.off(1)
    sleep(.01)

GPIO.cleanup()
