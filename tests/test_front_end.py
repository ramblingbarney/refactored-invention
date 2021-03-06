from app import app
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import game_operations
from collections import OrderedDict


class FlaskGameUITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("data/song_scores.txt", "w+") as text_file:
            print(f"conor,Placebo - Running Up That Hill,65", file=text_file)
            print(f"conor,Sinéad O'Connor - Nothing Compares 2U [Official Music Video],35", file=text_file)
            print(f"logan,Placebo - Running Up That Hill,95", file=text_file)
            print(f"logan,Sinéad O'Connor - Nothing Compares 2U [Official Music Video],35", file=text_file)

        with open("data/players.txt", "w+") as text_file:
            print(f"Tom,0,1", file=text_file)
            print(f"conor,100,0", file=text_file)
            print(f"logan,130,0", file=text_file)

    @classmethod
    def tearDownClass(cls):
        with open("data/song_scores.txt", "w+") as text_file:
            print(f"", file=text_file)

        with open("data/players.txt", "w+") as text_file:
            print(f"", file=text_file)

    def setUp(self):
        self.elements = []
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        # create selenium phantomjs instance
        self.driver = webdriver.PhantomJS(
            executable_path='/usr/local/bin/phantomjs',
            port=9134,
            service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])
        # set the browner window size
        self.driver.set_window_size(1079, 668)

    def tearDown(self):
        pass
        self.driver.quit()

    def test_home_status_code(self):
        ''' Test index/home page route'''
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_leaderboard_status_code(self):
        ''' Test leaderboard page route'''
        result = self.app.get('/leaderboard')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_whos_playing_status_code(self):
        ''' Test all_players page route'''
        result = self.app.get('/all_players')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_home_page_links(self):
        '''test the rendered page contains the Home, Leaderboard
            and Who's Playing text'''

        self.driver.get("http://localhost:5000")
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        for line in soup.find('div', {'id': 'navbarResponsive'}).find_all(
                'a', {'class': 'nav-link'}):
            self.elements.append(line.contents[0])
        self.assertIn('Home', self.elements)
        self.assertIn('Leaderboard', self.elements)
        self.assertIn("Who's Playing", self.elements)

    def test_home_page_game_rendering(self):
        '''test the rendered page contains the answer points'''
        self.driver.get("http://localhost:5000")
        time.sleep(3)
        html_tag_text = self.driver.find_element_by_id('answer-points').text
        assert "points" in html_tag_text
        self.assertIn('points', html_tag_text)

    def test_leaderboard_page_names(self):
        '''test the names rendered on the leaderboard page match the names
            in the order and value from the file'''

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_leaderboard(0)
        # convert keys to a list
        file_results_names = list(OrderedDict(file_results).keys())

        self.driver.get("http://localhost:5000/leaderboard")
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        for line in soup.find_all('div', {'class': 'leaderboard-name'}):
            self.elements.append(line.contents[0])

        self.assertListEqual(file_results_names, self.elements)

    def test_leaderboard_page_second_name_song_scores(self):
        '''test the second player individual songs from the
            file match leaderbaord page'''

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_leaderboard(0)
        # select the values as a list
        individual_songs = list(file_results.items())

        time.sleep(3)

        self.driver.get("http://localhost:5000/leaderboard")
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        for line in soup.find(
                'div', {'id': 'individual-song-scores2'}).find_all('li'):
                self.elements.append(line.contents[0].strip())
        self.assertListEqual(individual_songs[1][1], self.elements)

    def test_index_players_names(self):
        '''test the names rendered on the index/home page match the names in
            the order and value from the file'''

        # collect the names and song scores from the filename in OrderedDict
        file_results = game_operations.generate_leaderboard(4)
        # convert keys to a list
        file_results_names = list(OrderedDict(file_results).keys())

        self.driver.get("http://localhost:5000/")
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        for line in soup.find_all('div', {'class': 'leaderboard-name'}):
            self.elements.append(line.contents[0])

        self.assertListEqual(file_results_names, self.elements)

    def test_index_players_second_name_song_scores(self):
        '''test the second player individual songs from the file
            match leaderbaord page'''

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_leaderboard(4)

        # select the values as a list
        individual_songs = list(file_results.items())

        time.sleep(3)

        self.driver.get("http://localhost:5000/")
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')

        for line in soup.find(
                'div', {'id': 'individual-song-scores2'}).find_all('li'):
            self.elements.append(line.contents[0].strip())

        self.assertListEqual(individual_songs[1][1], self.elements)

    def test_all_players_page_names(self):
        '''test the names rendered on the All Players page match the names
            in the order and value from the file'''

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_logged_in_leaderboard(0)
        # convert keys to a list
        file_results_names = list(OrderedDict(file_results).keys())

        self.driver.get("http://localhost:5000/all_players")
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        for line in soup.find_all('div', {'class': 'leaderboard-name'}):
            self.elements.append(line.contents[0])

        self.assertListEqual(file_results_names, self.elements)

    def test_pagenotfound_statuscode(self):
        '''test the 404 status code when page is not found'''
        result = self.app.get('/missing-page')

        self.assertEqual(result.status_code, 404)

    def test_pagenotfound_data(self):
        '''test the 404 page content is shown when page is not found'''
        result = self.app.get('/missing-page')

        self.assertIn(b'We broke it, that page is missing', result.data)
