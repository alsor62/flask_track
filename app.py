from flask import Flask
import xls_read

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/track')
def track():
    return 'track!'


@app.route('/player')
def tr_player():
    xls_read.read_track()

    return 'End treck!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
