#!/usr/bin/env python

from time import sleep

import RPi.GPIO as GPIO
import random

CLOCK_PIN = 11
DATA_PIN = 12
LATCH_PIN = 13

GPIO.setmode(GPIO.BOARD)

GPIO.setup(CLOCK_PIN, GPIO.OUT)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)

GPIO.output(LATCH_PIN, 0)
GPIO.output(CLOCK_PIN, 0)
GPIO.output(DATA_PIN, 0)

for k in range(8):
    GPIO.output(LATCH_PIN, 0)
    GPIO.output(DATA_PIN, 0)

    print k

    for i in range(8):
        GPIO.output(CLOCK_PIN, 0)

        if i == k:
            GPIO.output(DATA_PIN, 1)
        else:
            GPIO.output(DATA_PIN, 0)

        GPIO.output(CLOCK_PIN, 1)

    GPIO.output(LATCH_PIN, 1)

    sleep(1)

GPIO.cleanup()
