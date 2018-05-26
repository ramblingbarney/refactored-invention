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

#error logging
logging.basicConfig(filename='log/guess_next_line.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger=logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

# list of video ids that have lyrics provided by musixmatch
pre_canned_videoId = ['YQHsXMglC9A','0-EF60neguk','MN3x-kAbgFU','YR5ApYxkU-U','n4RjJKxsamQ','raNGeq3_DtM','TvnYmWpD_T8','x5GuBa4Bbnw','4YR_Mft7yIM','JJAXwAaA2w','u1xrNaTO1bI','jhdFe3evXpk','YQHsXMglC9A']

@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":

        # This API request is being bypassed due to the chance that video id's returned are not music videos or are music videos but the lyrics are not available
        # If this project was to be made into a live service a library would have to be constructed of vidoes with lyrics by videoCategory

        '''
        payload = {'part': 'snippet', 'key': 'AIzaSyDBJyenwpSZ3BFota9_w0aueB2lj9fnl1M', 'chart': 'mostPopular' ,'maxResults': 10, 'videoCategory': '10'}
        l = requests.Session().get('https://www.googleapis.com/youtube/v3/videos', params=payload)
        resp_dict = json.loads(l.content)
        ytVideoId = resp_dict['items'][0]['id']
        print(resp_dict['items'][0]['id'])
        for i in range(len(resp_dict['items'])):
            print(resp_dict['items'][i]['id'])
        '''

        randomNumber = randint(0,len(pre_canned_videoId)- 1)

        try:

            rawlyric = music.fetch_srt('xxx',pre_canned_videoId[randomNumber])

            lyric = music.convert_srt(rawlyric)

            return render_template("index.html", page_title="Home", value=pre_canned_videoId[randomNumber],lyrics=lyric)

        except Exception as err:
            logger.error(err)
            return render_template('500.html'), 500

@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    if request.method == "POST":
        data = json.loads(request.data) # load JSON data from request

        score = str(game_operations.levestein_score(data['lyricAnswer'],data['stringToBeEvaluated']))
        return_data = {"score": score}

        response = app.response_class(
            response=json.dumps(return_data),
            status=200,
            mimetype='application/json'
        )
        return response

@app.route('/update_score', methods=['POST'])
def update_score():
    if request.method == "POST":
        data = json.loads(request.data) # load JSON data from request

        file_operations.update_file('data/players.txt', data['writeData'][0], data['writeData'][1])

        response = app.response_class(
            status=200,
            mimetype='application/json'
        )
        return response

@app.route('/song_score', methods=['POST'])
def song_total_score():
    if request.method == "POST":
        data = json.loads(request.data) # load JSON data from request

        file_operations.write_to_file('data/song_scores.txt',data['writeData']);

        response = app.response_class(
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        data = json.loads(request.data) # load JSON data from request

        result = file_operations.search_from_file('data/players.txt',data['userName'],0)

        if (result):

            return_data = result.split(',')

        else:

            file_operations.write_to_file('data/players.txt',data['userName'] + ',0')

            return_data = [data['userName'],0]

        response = app.response_class(
            response=json.dumps({'user_name':return_data[0], 'total_score':return_data[1]}),
            status=200,
            mimetype='application/json'
        )

        return response

@app.route('/all_players')
def all_players():
    return render_template("all_players.html")

@app.route('/leaderboard')
def leaderboard():

    template_values = game_operations.generate_leaderboard(0) # 0 option provides full results, called with interger option

    return render_template("leaderboard.html", names_classes=zip(template_values[0],template_values[1],template_values[2]))

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            debug=True)
