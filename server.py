#!/usr/bin/python2.7

import sys

sys.path.append('devices')

import socket
import RPi.GPIO as GPIO

from flask import Flask, render_template
from flask_socketio import SocketIO
from l293d import L293d
from math import ceil
import logging

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = False
socketio = SocketIO(app)
namespace = 'pibody'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

GPIO.setmode(GPIO.BOARD)

rightMotor = L293d(11, 12, 13)
leftMotor = L293d(18, 16, 15)

@app.route('/')
def index():
    return render_template('index.html', hostname=socket.gethostname())


@socketio.on('movement')
def handle_movement(message):
    toggled = message['toggled']
    x = message['x']
    y = message['y']

    if toggled:
        x_factor = (1 - abs((x * x * x) / 1000000.0))

        if x == 0:
            left_speed = y
            right_speed = y
        elif x > 0:
            right_speed = y
            if x >= 95:
                left_speed = -1 * right_speed
            else:
                left_speed = y * x_factor
        else:
            left_speed = y
            if x <= -95:
                right_speed = -1 * left_speed
            else:
                right_speed = y * x_factor

        rightMotor.move(right_speed)
        leftMotor.move(left_speed)

    else:
        rightMotor.stop()
        leftMotor.stop()


try:
    if __name__ == '__main__':
        socketio.run(app, host='0.0.0.0')

except (KeyboardInterrupt, SystemExit):
    GPIO.cleanup()
    raise
