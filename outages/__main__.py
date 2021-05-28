import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .provider import get_outages
from .calendar import write_calendar

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        outages = get_outages(driver)
    finally:
        driver.close()

    output_dir = "dist"
    os.makedirs(output_dir, exist_ok=True)
    write_calendar(outages, os.path.join(output_dir, "outages.ics"))
