from app import app
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import game_operations

class FlaskGameUITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        # create selenium phantomjs instance
        driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs'
        , port=9134, service_args=['--ignore-ssl-errors=true'
        , '--ssl-protocol=tlsv1'])

    def tearDown(self):
        pass
        driver.quit()

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_leaderboard_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/leaderboard')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_whos_playing_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/all_players')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_home_page_links(self):
        '''test the rendered page contains the Home, Leaderboard
            and Who's Playing text'''

        driver.get("http://localhost:5000")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source,'html5lib')
        elements = []
        for line in soup.find('div', {'id':'navbarResponsive'}).find_all('a',
            {'class': 'nav-link'}):
            elements.append(line.contents[0])
        self.assertIn('Home',elements)
        self.assertIn('Leaderboard',elements)
        self.assertIn("Who's Playing",elements)

    def test_home_page_game_rendering(self):
        '''test the rendered page contains the answer points'''
        driver.get("http://localhost:5000")
        time.sleep(3)
        html_tag_text = driver.find_element_by_id('answer-points').text
        assert "points" in html_tag_text

    def test_leaderboard_page_names(self):
        '''test the names rendered on the leaderboard page match the names in the order and value from the file'''

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_leaderboard(0)
        #test the rendered page contains the Home, Leaderboard and Who's Playing text
        driver.get("http://localhost:5000/leaderboard")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source,'html5lib')
        elements = []
        for line in soup.find_all('div', {'class':'leaderboard-name'}):
            elements.append(line.contents[0])

        self.assertListEqual(file_results[0], elements)

    def test_leaderboard_page_second_name_song_scores(self):
        '''test the second player individual songs from the
            file match leaderbaord page'''

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_leaderboard(0)
        line_list = file_results[2][1].replace('<li>','').split('</li>')
        del line_list[-1]
        time.sleep(3)

        driver.get("http://localhost:5000/leaderboard")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source,'html5lib')
        elements = []
        for line in soup.find('div', {'id':'individual-song-scores2'}).find_all('li'):
            elements.append(line.contents[0].strip())
        self.assertListEqual(line_list, elements)

    def test_top_players_names(self):
        '''test the names rendered on the home page match the names in
            the order and value from the file'''

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_leaderboard(4)
        # test the rendered page contains the Home, Leaderboard and Who's Playing text
        driver.get("http://localhost:5000/")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source,'html5lib')
        elements = []
        for line in soup.find_all('div', {'class':'top-player-name'}):
            elements.append(line.contents[0])
        self.assertListEqual(file_results[0], elements)

    def test_top_players_second_name_song_scores(self):
        # test the second player individual songs from the file match leaderbaord page

        # collect the names, classes and song scores from the filename
        file_results = game_operations.generate_leaderboard(4)
        line_list = file_results[2][1].replace('<li>','').split('</li>')
        del line_list[-1]
        time.sleep(3)

        driver.get("http://localhost:5000/")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source,'html5lib')
        elements = []
        for line in soup.find('div', {'id':'individual-song-scores2'}).find_all('li'):
            elements.append(line.contents[0].strip())
        self.assertListEqual(line_list, elements)
