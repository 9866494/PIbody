from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app)
namespace = 'pibody'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('movement')
def handle_movement(message):
    print(message)

try:
    if __name__ == '__main__':
        socketio.run(app, host='0.0.0.0')

except (KeyboardInterrupt, SystemExit):
    raise
