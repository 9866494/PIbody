#!/usr/bin/env python

# Class to control the 28BJY-48 stepper motor with ULN2003 control board.
# Converted from work done by Stephen Phillips (www.scphillips.com)

from time import sleep
from threading import Thread
import RPi.GPIO as GPIO

class Motor:
    def __init__(self, pins, revs_per_minute, initial_angle = 0):
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]

        self.deg_per_step = 5.625 / 64
        self.steps_per_rev = int(360 / self.deg_per_step)
        self.step_angle = 8 * (int(initial_angle / self.deg_per_step) / 8)
        self._rpm = revs_per_minute

        self._T = (60.0 / self._rpm) / self.steps_per_rev

    def _move_to_short(self, angle):
        target_step_angle = 8 * (int(angle / self.deg_per_step) / 8)
        steps = target_step_angle - self.step_angle
        steps = int(steps % self.steps_per_rev)

        if steps > self.steps_per_rev / 2:
            steps -= int(self.steps_per_rev)
            self._move_acw(-steps / 8)
        else:
            self._move_cw(steps / 8)

    def _move_to(self, angle):
        target_step_angle = 8 * (int(angle / self.deg_per_step) / 8)
        steps = target_step_angle - self.step_angle

        print(self.step_angle)
        print(target_step_angle)

        if steps > 0:
            print("acw")
            self._move_acw(steps / 8)
        else:
            print("cw")
            self._move_cw(-steps / 8)

    def _on_move_step(self, steps):
        self.step_angle += steps
        sleep(self._T)
        return True

    def _move_cw(self, big_steps):
        big_steps = int(big_steps)

        for i in range(big_steps):
            GPIO.output(self.P4, 1)
            if not self._on_move_step(-1): break
            GPIO.output(self.P2, 0)
            if not self._on_move_step(-1): break
            GPIO.output(self.P3, 1)
            if not self._on_move_step(-1): break
            GPIO.output(self.P1, 0)
            if not self._on_move_step(-1): break
            GPIO.output(self.P2, 1)
            if not self._on_move_step(-1): break
            GPIO.output(self.P4, 0)
            if not self._on_move_step(-1): break
            GPIO.output(self.P1, 1)
            if not self._on_move_step(-1): break
            GPIO.output(self.P3, 0)
            if not self._on_move_step(-1): break

        self.stop()

    def _move_acw(self, big_steps):
        big_steps = int(big_steps)

        for i in range(big_steps):
            GPIO.output(self.P3, 0)
            if not self._on_move_step(1): break
            GPIO.output(self.P1, 1)
            if not self._on_move_step(1): break
            GPIO.output(self.P4, 0)
            if not self._on_move_step(1): break
            GPIO.output(self.P2, 1)
            if not self._on_move_step(1): break
            GPIO.output(self.P1, 0)
            if not self._on_move_step(1): break
            GPIO.output(self.P3, 1)
            if not self._on_move_step(1): break
            GPIO.output(self.P2, 0)
            if not self._on_move_step(1): break
            GPIO.output(self.P4, 1)
            if not self._on_move_step(1): break

        self.stop()

    def stop(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

    def test(self):
        self.move_to(180)
        sleep(.3)
        self.move_to(0)

class SyncMotor(Motor):
    def move_to(self, angle):
        self._move_to(angle)

    def move_to_short(self, angle):
        self._move_to_short(angle)

class AsyncMotor(Motor):
    def __init__(self, pins, revs_per_minute, initial_angle = 0):
        Motor.__init__(self, pins, revs_per_minute, initial_angle = 0)
        self.thread = Thread(target=self._wait_for_movement)
        self._move_to_angle = initial_angle
        self._thread_running = True
        self._angle_changed = False
        self._stoped = True
        self.thread.start()
        self.thread.join()

    def _wait_for_movement(self):
        while self._thread_running:
            if self._angle_changed and self._stoped:
                self._angle_changed = False
                self._stoped = False
                self._move_to(self._move_to_angle)
            sleep(0.01)

    def move_to(self, angle):
        self._angle_changed = True
        self._move_to_angle = angle

    def _on_move_step(self, steps):
        Motor._on_move_step(self, steps)
        if self._angle_changed:
            return False
        else:
            return True

    def stop(self):
        Motor.stop(self)
        self._stoped = True

    def stop_thread(self):
        self.stop()
        self._thread_running = False



GPIO.setmode(GPIO.BOARD)
m = AsyncMotor([11,12,13,15], 15, 0)
m.test()
sleep(5)
m.stop_thread()
GPIO.cleanup()
