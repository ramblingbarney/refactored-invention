from app import app
import unittest
from selenium import webdriver
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

    def test_home_page(self):
        # test the rendered page contains the hello world text
        driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', port=9134, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])
        driver.get("http://localhost:5000")
        time.sleep(3)
        html_tag_text = driver.find_element_by_tag_name('p').text
        assert "Hello world!" in html_tag_text
        driver.quit
