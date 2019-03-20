from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json


DEBUG = True
PORT = 8000

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/main')
def main():
    with open('topics.json') as topics_data:
        topics = json.load(topics_data)
        with open('events.json') as events_data:
            events = json.load(events_data)
            return render_template('main.html', topics=topics, events=events)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)