#!/usr/bin/python

import flask
from flask import request, jsonify
import threading
import time
import requests

app = flask.Flask(__name__)

@app.before_first_request
def activate_job():
    def run_job():
        while True:
                #print("hello\n")
                time.sleep(2)

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/', methods=['GET'])
def hello():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/led/<color>/', methods=["GET","POST"])
def api_id(color):
    if request.method == "POST":
        s = request.get_json()
        state = int(s.get('state'))
        print(color, " ", state, " is requested")
        data = {"state":"{}".format(state)}
        resp = requests.post('http://raspberry/led/{}/'.format(color), json=data)
    else:
        print("no state found")
        return "Error: No state provided for LED."
    return jsonify({color: state})

if __name__ == "__main__":
    app.run(debug=True, port=5555, host='0.0.0.0')
