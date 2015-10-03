#!/usr/bin/env python

import sys
sys.path.append('devices')

from gevent import monkey
monkey.patch_all()

import RPi.GPIO as GPIO
import time
from threading import Thread
from flask import Flask, render_template, send_from_directory, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect
from stepper import AsyncMotor

try:
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)
    namespace = 'robo'

    GPIO.setmode(GPIO.BOARD)
    m = AsyncMotor([11,12,13,15], 15)

    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('/static/js', path)

    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('led_shim', namespace= namespace)
    def test_message(message):
        emit('led_shim response',
             {'data': message['value']}
             )


    @socketio.on('cam_rotate', namespace= namespace)
    def test_message(message):
        m.stop()
        m.move_to(float(message['value']))
        emit('cam_rotate response',
             {'data': message['value']}
             )

    @socketio.on('disconnect request', namespace=namespace)
    def disconnect_request():
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my response',
             {'data': 'Disconnected!', 'count': session['receive_count']}
             )
        disconnect()


    @socketio.on('connect', namespace= namespace)
    def test_connect():
        emit('my response',
            {'data': 'Connected', 'count': 0}
            )


    @socketio.on('disconnect', namespace= namespace)
    def test_disconnect():
        print('Client disconnected')


    if __name__ == '__main__':
        socketio.run(app,host='0.0.0.0')

except (KeyboardInterrupt, SystemExit):
    GPIO.cleanup()
    raise
