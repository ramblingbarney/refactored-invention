from app import app
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class FlaskBookshelfTests(unittest.TestCase):

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

    def tearDown(self):
        pass

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
        # test the rendered page contains the hello world text
        driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', port=9134, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])
        driver.get("http://localhost:5000")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source,'html5lib')
        elements = []
        for line in soup.find('div', {'id':'navbarResponsive'}).find_all('a', {'class': 'nav-link'}):
            elements.append(line.contents[0])
        assert "Home" in elements
        assert "Leaderboard" in elements
        assert "Who's Playing" in elements
        driver.quit

    def test_home_page_game_rendering(self):
        # test the rendered page contains the hello world text
        driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', port=9134, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])
        driver.get("http://localhost:5000")
        time.sleep(3)
        html_tag_text = driver.find_element_by_id('answer-points').text
        print(html_tag_text)
        assert "points" in html_tag_text
        driver.quit
