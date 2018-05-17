# Stream 2A Flask application

This README outlines the details of collaborating on this Ember application.
This application is a game where the user guesses the next lyric that the video will plays

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](https://git-scm.com/)
* [Python3](https://www.python.org/) (with HomeBrew & Venv)
* [Google Chrome](https://google.com/chrome/)

## Installation

* `git clone git@github.com:ramblingbarney/refactored-invention.git` this repository
* `cd refactored-invention`
* `pip3 install -r /path/to/requirements.txt`

### Running Tests

* Download the latest phantomjs binary: http://phantomjs.org, update line 52 of 'test_front_end.py' to the location of the pantomjs binary
* `phantomjs-1.9.8-linux-x86_64/bin/phantomjs --webdriver=9134`
* `python3 -m unittest tests/test_front_end.py`

## Acceptance tests

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

## Manual Testing

  * Login & Logout.
    * Enter a username in input box and click 'Login', verify the navigation bar shows the username and points for the username.
    * Refresh the page and verify the currently logged in user is still shown in the navigation bar.
    * Click 'Logout' and verify the navigation bar no longer shows a username and points.

  * Logged in users Total Score and Total Song Score
    * Enter username in login box, click login, start song stream and enter an answer, it will be evaluated and a score applied which will then be shown in the 'Total Song Points' and the user's points in the navigation bar.
    * Logout, then login and the users updated score will be shown in the navigation bar.


## Known Issues

* On small screens the login/logout text box will reduce in width so the text cannot been seen and the logout button can be forced to the next line in some instances.
* The API call to musixmatch fails causing the error 500 page to be shown which will fail the test as well.
* PouchDB is not encrypted so will be accessable to all in the browser
* Flask passes variable data to the template which is displayed in page source
* Clicking play on the video will play in full screen on iphone mobile browser with prevents the user entering the answers
