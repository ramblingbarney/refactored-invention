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

* As a user I want to see navigatin icons in the menu bar on the home page.

  * Example acceptance criteria:
    * 'Home' link on the 'Home' page
    * 'Leaderboard' link on the 'Home' page
    * 'Who's Playing' link on the 'Home' page
    * Clicking 'Leaderboard' link take you to the 'Leaderboard' page.
    * Clicking 'Who's Playing' link take you to the 'Who's Playing' page.



## Known Issues

* On small screens the login/logout text box will reduce in width so the text cannot been seen
