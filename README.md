# Stream 2A Flask application

The purpose of this application is to provide a proof of concept for a game where the user guesses the next line of the song being streamed.  

Once the page is loaded the game is ready to play, click play on the video iframe and enter the song lyrics in the text box on the right of the video in desktop mode or for smaller screens below the video.

To login enter a username in the nav bar input box and your song scores and total scores will be recorded and displayed on the page.  The game is queued to play a random selection from 15 videos, to start another game refresh the home/index page.

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](https://git-scm.com/)
* [Python3](https://www.python.org/) (with HomeBrew & Venv)
* [Google Chrome](https://google.com/chrome/)

## Installation

* ```git clone git@github.com:ramblingbarney/refactored-invention.git```
* ```cd refactored-invention```
* ```pip3 install -r /path/to/requirements.txt```

### Running Tests

* Download the latest phantomjs binary: http://phantomjs.org, update line 52 of 'test_front_end.py' to the location of the pantomjs binary.
* ```phantomjs-1.9.8-linux-x86_64/bin/phantomjs --webdriver=9134```
* ```python3 -m unittest tests/test_front_end.py```
* ```python3 -m unittest tests/test_back_end.py```

## Acceptance tests

### All Pages

### Top Players User Stories

* As a user I want to see the top 4 players with scores from left to right using a different colour.

  * Example acceptance criteria:
    *  Each player that has created a login and scored at least one point will be shown
    *  Each player that has completed a song with a sore will have it listed below their name when you click 'View Scores'

### Home Page User Stories

* As a user I want to see navigation icons in the menu bar on the home page.

  * Example acceptance criteria:
    * 'Home' link on the 'Home' page
    * 'Leaderboard' link on the 'Home' page
    * 'Who's Playing' link on the 'Home' page
    * Clicking 'Leaderboard' link take you to the 'Leaderboard' page.
    * Clicking 'Who's Playing' link take you to the 'Who's Playing' page.

* As a user I want to click on the video iframe and the video to start Playing
  * Example acceptance criteria:
    * Video Plays
    * At timed intervals the lyrics are shown in blue text
    * The answers are scored and the points awarded are shown below the answer.

* As a user I want to see a warning message on the page if cookies are disabled in the browser
  * Example acceptance criteria:
    * Warning message is shown asking user to enable cookies

### Leaderboard Page User Stories

* As a user I want to see a list of all players with scores from left to right using a different colour.

  * Example acceptance criteria:
    *  Each player that has created a login and scored at least one point will be shown
    *  Each player that has completed a song with a sore will have it listed below their name when you click 'View Scores'

* As a user I want to see a warning message on the page if cookies are disabled in the browser
    * Example acceptance criteria:
    * Warning message is shown asking user to enable cookies

### All Players User Stories

* As a user I want to see a warning message on the page if cookies are disabled in the browser
    * Example acceptance criteria:
    * Warning message is shown asking user to enable cookies

## Manual Testing

  * Login & Logout.
    * Enter a username in input box and click 'Login', verify the navigation bar shows the username and points for the username.
    * Refresh the page and verify the currently logged in user is still shown in the navigation bar.
    * Click 'Logout' and verify the navigation bar no longer shows a username and points.

  * Logged in users Total Score and Total Song Score
    * Enter username in login box, click login, start song stream and enter an answer, it will be evaluated and a score applied which will then be shown in the 'Total Song Points' and the user's points in the navigation bar.
    * Logout, then login and the users updated score will be shown in the navigation bar.

  * Leaderboard
    * execute this command 'cat data/players.txt' and ensure the order left to right reflects the highest to lowest player scores shown
    * execute this command 'cat data/song_scores.txt' and ensure the songs listed with the username in the first column are correctly assigned to the user 'View Scores'

  * Cookie Warning
    * Disable cookies in the browser settings and then navigate to the index, all players and leaderboard pages and check to see if working message is shown at the top

## Known Issues

* On small screens the login/logout text box will reduce in width so the text cannot been seen and the logout button can be forced to the next line in some instances.
* When the login input box is empty clicking login will log in the last user
* The API call to musixmatch fails causing the error 504 page to be shown which will fail the test suite as well.
* PouchDB is not encrypted so will be accessable to all in the browser
* Flask passes variable data to the template which is displayed in page source
* Clicking play on the video will play in full screen on iphone mobile browser with prevents the user entering the answers

## Code removed for existing version

This API request is being bypassed due to the chance that video id's returned are not music videos or are music videos but the lyrics are not available.

If this project was to be made into a live service a library would have to be constructed of vidoes with lyrics by videoCategory

payload = {'part': 'snippet', 'key': 'AIzaSyDBJyenwpSZ3BFota9_w0aueB2lj9fnl1M', 'chart': 'mostPopular' ,'maxResults': 10, 'videoCategory': '10'}
l = requests.Session().get('https://www.googleapis.com/youtube/v3/videos', params=payload)
resp_dict = json.loads(l.content)
ytVideoId = resp_dict['items'][0]['id']

for i in range(len(resp_dict['items'])):
  print(resp_dict['items'][i]['id'])
