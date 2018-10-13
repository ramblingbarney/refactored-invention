import os
import sys
from flask import Flask, render_template, redirect, request, jsonify
import json
import requests
import music
import file_operations
import game_operations
from random import randint, random

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


# list of video ids that have lyrics provided by musixmatch
pre_canned_videoId = [
    'YQHsXMglC9A', '0-EF60neguk', 'MN3x-kAbgFU', 'YR5ApYxkU-U',
    'n4RjJKxsamQ', 'raNGeq3_DtM', 'TvnYmWpD_T8', 'x5GuBa4Bbnw',
    '4YR_Mft7yIM', 'JJAXwAaA2w', 'u1xrNaTO1bI', 'jhdFe3evXpk',
    'YQHsXMglC9A']


@app.route('/')
def index():
    '''
    Home page and the page to play the game
    '''

    # see README.md for google API code which would be used instead of below
    # in production version

    random_number = randint(0, len(pre_canned_videoId) - 1)

    try:
        raw_lyric = music.fetch_srt('xxx', pre_canned_videoId[random_number])
        lyric = music.convert_srt(raw_lyric)
        # get a list of 4 players and songs for the top scores section
        template_users_history = game_operations.generate_leaderboard(4)
        return render_template(
            "index.html",
            page_title="Home",
            value=pre_canned_videoId[random_number],
            lyrics=lyric,
            users_history=template_users_history)
    except Exception as e:
        return render_template("504.html", error=str(e))


@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    '''
    Score the answer string of the user playing end point
    '''

    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)
        score = str(
            game_operations.levenshtein_score(
                data['lyricAnswer'], data['stringToBeEvaluated']))
        answer_score = {"score": score}
        response = app.response_class(
            response=json.dumps(answer_score),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/update_score', methods=['POST'])
def update_score():
    '''
    Update the total score of the current logged in player end point
    '''

    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)
        # Update players file with username, total score and zero to denote
        # user is logged out
        file_operations.update_file(
            'data/players.txt',
            data['writeData'][0],
            data['writeData'][1] + ',0')
        response = app.response_class(
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/song_score', methods=['POST'])
def song_total_score():
    '''
    Save total song score end point
    '''

    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)
        file_operations.write_to_file(
            'data/song_scores.txt', data['writeData'])
        response = app.response_class(
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/login', methods=['POST'])
def login():
    '''
    Login end point
    '''

    if request.method == "POST":
        # load JSON data from request
        data = json.loads(request.data)
        # search for user's player record, returning a single line '0' switch
        player_record = file_operations.search_from_file(
            'data/players.txt', data['userName'], 0)

        if (player_record):
            username_score = player_record.split(',')
            # update players file with username, total score, 1 switch denotes
            # user is logged in
            file_operations.update_file(
                'data/players.txt',
                username_score[0],
                username_score[1] + ',1')
        else:
            # write new user to file username, 0 total score and 1 switch
            # denotes user is logged in
            file_operations.write_to_file(
                'data/players.txt', data['userName'] + ',0' + ',1')
            username_score = [data['userName'], 0]

        response = app.response_class(
                    response=json.dumps({
                        'user_name': username_score[0],
                        'total_score': username_score[1]}),
                    status=200,
                    mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/all_players')
def all_players():
    '''
    Show all current logged in players with their scores by song
    '''

    template_users_history = game_operations.generate_logged_in_leaderboard(0)
    return render_template(
        "all_players.html", users_history=template_users_history)


@app.route('/leaderboard')
def leaderboard():
    '''
    Show all player scores by song
    '''

    # generate_leaderboard with '0' option provides full results
    # generate_leaderboard with a interger greater than zero returns that
    # number of results or the total number availabe where
    # this is a lower number
    template_users_history = game_operations.generate_leaderboard(0)
    return render_template(
        "leaderboard.html", users_history=template_users_history)


@app.errorhandler(Exception)
def unhandled_exception(e):
    '''
    Renders custom error page for all errors caused by
    network connection or code errors
    '''

    app.logger.error('Unhandled Exception: %s', (e))
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), debug=False)
