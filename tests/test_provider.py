import unittest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from outages.provider import get_outages


class TestProvider(unittest.TestCase):
    def test_integration(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        try:
            outages = get_outages(driver)
        finally:
            driver.close()

        self.assertIsNotNone(outages)
