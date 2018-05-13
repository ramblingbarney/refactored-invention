import os
import sys
import logging
from flask import Flask, render_template, redirect, request, jsonify


app = Flask(__name__)

# error logging
logging.basicConfig(filename='log/guess_next_line.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger=logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

@app.route('/')
def index():
    return render_template("index.html", page_title="Home")

@app.route('/all_players')
def all_players():
    return render_template("all_players.html")

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            debug=True)
