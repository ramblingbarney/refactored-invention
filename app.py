import os
import sys
import logging
from flask import Flask, render_template, redirect, request, jsonify
import json
import requests
import music
import file_operations
import game_operations
from random import randint, random

app = Flask(__name__)
app.secret_key = 'aEP#gtR}isb2vG*={o-ui_WR6X9*<72NCe8CN7Ej6fMAyIOIlr'

# list of video ids that have lyrics provided by musixmatch
pre_canned_videoId = ['YQHsXMglC9A', '0-EF60neguk', 'MN3x-kAbgFU'
                    , 'YR5ApYxkU-U', 'n4RjJKxsamQ', 'raNGeq3_DtM'
                    , 'TvnYmWpD_T8', 'x5GuBa4Bbnw', '4YR_Mft7yIM'
                    , 'JJAXwAaA2w', 'u1xrNaTO1bI', 'jhdFe3evXpk'
                    , 'YQHsXMglC9A']


@app.route('/')
def index():

    # see README.md for google API code which would be used instead of below
    # in production version

    random_number = randint(0, len(pre_canned_videoId) - 1)

    raw_lyric = music.fetch_srt('xxx', pre_canned_videoId[random_number])

    lyric = music.convert_srt(raw_lyric)

    # get a list of 4 players and songs for the top scores section
    template_name_songs = game_operations.generate_leaderboard(4)

    return render_template("index.html", page_title="Home"
                            , value=pre_canned_videoId[random_number]
                            , lyrics=lyric
                            , names_songs=zip(template_name_songs[0]
                            , template_name_songs[1]))


@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)

        score = str(game_operations.levenstein_score(data['lyricAnswer']
                    , data['stringToBeEvaluated']))

        answer_score = {"score": score}

        response = app.response_class(
            response=json.dumps(answer_score),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/update_score', methods=['POST'])
def update_score():
    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)

        file_operations.update_file('data/players.txt', data['writeData'][0]
                                    , data['writeData'][1])

        response = app.response_class(
            status=200,
            mimetype='application/json'
        )
        return response

@app.route('/song_score', methods=['POST'])
def song_total_score():
    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)

        file_operations.write_to_file('data/song_scores.txt'
                                    , data['writeData'])

        response = app.response_class(
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)

        result = file_operations.search_from_file('data/players.txt'
                    , data['userName'],0)

        if (result):

            username_score = result.split(',')

        else:

            file_operations.write_to_file('data/players.txt'
                , data['userName'] + ',0')

            username_score = [data['userName'], 0]

        response = app.response_class(
            response=json.dumps({'user_name': username_score[0]
                                , 'total_score': username_score[1]}), status=200
                                , mimetype='application/json')

        return response


@app.route('/all_players')
def all_players():

    return render_template("all_players.html")


@app.route('/leaderboard')
def leaderboard():

    # generate_leaderboard with '0' option provides full results
    # generate_leaderboard with a interger greater than zero returns that
    # number of results or the total number availabe where
    # this is a lower number

    template_users_history = game_operations.generate_leaderboard(0)

    return render_template("leaderboard.html"
                            , users_history=template_users_history)


@app.errorhandler(504)
def gateway_time_out(e):
    return render_template('504.html'), 504


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            debug=True)
