# Stream 2A Flask application

The purpose of this application is to provide a proof of concept for a game where the user guesses the next line of the song being streamed.  

Once the page is loaded the game is ready to play, click play on the video iframe and enter the song lyrics in the text box on the right of the video in desktop mode or for smaller screens below the video.

To login enter a username in the nav bar input box and your song scores and total scores will be recorded and displayed on the page.  The game is queued to play a random selection from 15 videos, to start another game refresh the home/index page.

## Prerequisites

You will need the following things properly installed on your computer.

* [Python3](https://www.python.org/)

## Wireframes

* [Pencil](http://pencil.evolus.vn) (wireframes/guess_the_next_line_0-0.epgz wireframes/index.html)

## Installation

* ```pip3 install -r /path/to/requirements.txt```
* ```export SECRET_KEY=< add complex string>```

## Deployment
The 'development' and 'testing' of the app have been done on the 'master' branch.

The deployed version (master_heroku) on heroku has the following differences from the 'master' branch

### Additional modules

* 'from flask_cors import CORS, cross_origin'

### Setup

* app.config['CORS_HEADERS'] = 'Content-Type'
* cors = CORS(app, resources={r"/\*": {"origins": "guess-the-next-line.herokuapp.com"}})

### Heroku configuration variables

* SECRET_KEY

### Heroku config files

* runtime.txt
* Procfile
* requirements.txt

### Running Tests

* Download the latest phantomjs binary: http://phantomjs.org, update line 52 of 'test_front_end.py' to the location of the pantomjs binary.
* ```phantomjs-1.9.8-linux-x86_64/bin/phantomjs --webdriver=9134```
* ```python3 -m unittest tests/test_front_end.py```
* ```python3 -m unittest tests/test_back_end.py```

## Acceptance tests

### All Pages

### Top Players User Stories

* As a user I want to see the top 4 players with scores from left to right using a different colour.

  * Acceptance criteria:
    *  Each player that has created a login will be shown
    *  Each player that has completed a song with a sore will have it listed below their name when you click 'View Scores'

### Home Page User Stories

* As a user I want to see navigation icons in the menu bar on the home page.

  * Acceptance criteria:
    * 'Home' link on the 'Home' page
    * 'Leaderboard' link on the 'Home' page
    * 'Who's Playing' link on the 'Home' page
    * Clicking 'Leaderboard' link take you to the 'Leaderboard' page.
    * Clicking 'Who's Playing' link take you to the 'Who's Playing' page.

* As a user I want to click on the video iframe and the video to start Playing
  * Acceptance criteria:
    * Video Plays
    * At timed intervals the lyrics are shown in blue text
    * The answers are scored and the points awarded are shown below the answer.

* As a user I want to see a warning message on the page if cookies are disabled in the browser
  * Acceptance criteria:
    * Warning message is shown asking user to enable cookies

* As a user I want to see a list of all players with scores from left to right using a different colour.
  * Acceptance criteria:
    *  Each player that has created a login will be shown
    *  Each player that has completed a song with a sore will have it listed below their name when you click 'View Scores'

### Leaderboard Page User Stories

* As a user I want to see a list of all players with scores from left to right using a different colour.
  * Acceptance criteria:
    *  Each player that has created a login will be shown
    *  Each player that has completed a song with a sore will have it listed below their name when you click 'View Scores'

* As a user I want to see a warning message on the page if cookies are disabled in the browser
  * Acceptance criteria:
    * Warning message is shown asking user to enable cookies

### All Players User Stories

* As a user I want to see a warning message on the page if cookies are disabled in the browser
  * Acceptance criteria:
    * Warning message is shown asking user to enable cookies

* As a user I want to see a list of all players with scores from left to right using a different colour who are currently logged in.
  * Acceptance criteria:
    *  Each player that is logged in will be shown
    *  Each player that has completed a song with a sore will have it listed below their name when you click 'View Scores'

## Manual Testing

  * Login & Logout.
    * Enter a username in input box and click 'Login', verify the navigation bar shows the username and points for the username.
    * Refresh the page and verify the currently logged in user is still shown in the navigation bar.
    * Click 'Logout' and verify the navigation bar no longer shows a username and points.
    * When the user is logged in, the players.txt file will have a final column with a value of 1 and 0 when logged out, to check ```cat data/players.txt```

  * Logged in users Total Score and Total Song Score
    * Enter username in login box, click login, start song stream and enter an answer, it will be evaluated and a score applied which will then be shown in the 'Total Song Points' and the user's points in the navigation bar.
    * Logout, then login and the users updated score will be shown in the navigation bar.

  * Leaderboard
    * execute this command 'cat data/players.txt' and ensure the order left to right reflects the highest to lowest player scores shown
    * execute this command 'cat data/song_scores.txt' and ensure the songs listed with the username in the first column are correctly assigned to the user 'View Scores'

  * Who's Playing (All Players)
    * execute this command 'cat data/players.txt' and ensure the order left to right reflects the highest to lowest player scores shown for only those lines ending with a '1'
    * execute this command 'cat data/song_scores.txt' and ensure the songs listed with the username in the first column are correctly assigned to the user 'View Scores'

  * Cookie Warning
    * Disable cookies in the browser settings and then navigate to the index, all players and leaderboard pages and check to see if working message is shown at the top

  * Force timeout for index page
    * Turn off the internet connection and refresh the index page.  Check the 504 page is shown with the text "Whoops  We broke it, lets try again"

## Known Issues

  * On small screens the login/logout text box will reduce in width so the text cannot been seen and the logout button can be forced to the next line in some instances.
  * When the login input box is empty clicking login will log in the last user
  * On Android & iOS mobile devices the login will not work, no error is thrown but the page will not show a user logged in
  * After login a page refresh is required to update the UI, the refresh triggers the getCookieName function which updates the UI
  * The login route has response headers set to response.headers['Access-Control-Allow-Origin'] = * to circumvent the browser COR security check
  * Logging in during a game will cause the total score for the user not to be equal to sum total of individual song scores because the song score is only recorded when the video has completed playing
  * The API call to musixmatch fails/timesout causing the error 504 page to be shown which will fail the test suite as well.
  * The video may not load so the page is rendered but the video iframe has a failed error message
  * PouchDB is not encrypted so will be accessable to all in the browser
  * Flask passes variable data to the template which is displayed in page source
  * Clicking play on the video will play in full screen on iphone mobile browser with prevents the user entering the answers
  * The game will not evaluate answers on Android 8 devices using the chrome browser, the game will operate as expected on Android 7 devices using the chrome browser


## Code removed for existing version

This API request is being bypassed due to the chance that video id's returned are not music videos or are music videos but the lyrics are not available.

If this project was to be made into a live service a library would have to be constructed of vidoes with lyrics by videoCategory

payload = {'part': 'snippet', 'key': 'AIzaSyDBJyenwpSZ3BFota9_w0aueB2lj9fnl1M', 'chart': 'mostPopular' ,'maxResults': 10, 'videoCategory': '10'}
l = requests.Session().get('https://www.googleapis.com/youtube/v3/videos', params=payload)
resp_dict = json.loads(l.content)
ytVideoId = resp_dict['items'][0]['id']

for i in range(len(resp_dict['items'])):
  print(resp_dict['items'][i]['id'])
