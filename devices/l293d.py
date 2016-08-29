#!/usr/bin/env python

from time import sleep

import RPi.GPIO as GPIO

class L293d:
    speed = 100

    def __init__(self, forward_pin, backward_pin, speed_pin):
        self.FORWARD_PIN = forward_pin
        self.BACKWARD_PIN = backward_pin
        self.SPEED_PIN = speed_pin

        GPIO.setup(self.FORWARD_PIN, GPIO.OUT)
        GPIO.setup(self.BACKWARD_PIN, GPIO.OUT)
        GPIO.setup(self.SPEED_PIN, GPIO.OUT)

        self.stop()

        self.speed_pwm = GPIO.PWM(self.SPEED_PIN, self.speed)
        self.speed_pwm.start(1)

    def stop(self):
        GPIO.output(self.BACKWARD_PIN, 0)
        GPIO.output(self.FORWARD_PIN, 0)

    def forward(self, speed = None):
        self.setSpeed(speed)
        GPIO.output(self.BACKWARD_PIN, 0)
        GPIO.output(self.FORWARD_PIN, 1)

    def backward(self, speed = None):
        self.setSpeed(speed)
        GPIO.output(self.BACKWARD_PIN, 1)
        GPIO.output(self.FORWARD_PIN, 0)

    def setSpeed(self, speed):
        if (speed):
            if speed > 100:
                speed = 100
            elif speed <= 10:
                speed = 10

            self.speed_pwm.ChangeDutyCycle(speed)
            self.speed = speed
        else:
            self.speed_pwm.ChangeDutyCycle(self.speed)


GPIO.setmode(GPIO.BOARD)

l293d = L293d(11,12,13)

l293d.forward(2000)
sleep(2)
l293d.backward(-1)
sleep(2)

GPIO.cleanup()
