from time import sleep
from random import randint, random

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

    def move(self, speed = None):
        if speed > 0:
            self.forward(abs(speed))
        else:
            self.backward(abs(speed))

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

            if self.speed != speed:
                self.speed_pwm.ChangeDutyCycle(speed)
                self.speed = speed

    def test(self):
        for fwd in range(randint(0,25)):
            self.forward(randint(0,100))
            sleep(random())

        for fwd in range(randint(0,25)):
            self.backward(randint(0,100))
            sleep(random())

        self.stop()
