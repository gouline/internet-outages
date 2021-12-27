import logging
import os
from typing import List
import dateparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .outage import Outage


class ProviderOutage(Outage):
    """Provider-specific outage container."""

    def __init__(self):
        super().__init__()
        self.name = "Provider outage"

    def put_attribute(self, title: str, value: str):
        """Put one attribute as it's parsed.

        Args:
            title (str): Attribute title.
            value (str): Attribute value.
        """

        key = title.lower()

        if key in ("start", "end"):
            value = dateparser.parse(value)

        if key == "severity":
            self.severity = value
        elif key == "start":
            self.start = value
        elif key == "end":
            self.end = value
        else:
            logging.warning("Unknown attribute: %s", key)


def get_outages(driver: webdriver.Chrome) -> List[Outage]:
    """Retrieves the outages from the website.

    Args:
        driver (webdriver.Chrome): Configured web driver.

    Returns:
        List[Outage]: List of outages.
    """

    username = os.getenv("PROVIDER_USERNAME")
    password = os.getenv("PROVIDER_PASSWORD")

    driver.get("https://gouline.github.io/outages-sample/provider/login.html")
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_tag_name("form").submit()

    WebDriverWait(driver, 10).until(EC.title_contains("Outages"))

    outages = []

    for list_group_item in driver.find_elements_by_class_name("list-group-item"):
        outage = ProviderOutage()

        for container in list_group_item.find_elements_by_class_name("container"):
            try:
                strong = container.find_element_by_tag_name("strong")
            except NoSuchElementException:
                continue

            title = strong.text.strip()
            value = container.text.replace(title, "").strip()
            outage.put_attribute(title, value)

        try:
            em = list_group_item.find_element_by_tag_name("em")
            outage.uid = em.text.replace("#", "")
        except NoSuchElementException:
            logging.warning("No em ID found")

        try:
            subtitle = list_group_item.find_element_by_class_name("subtitle")
            outage.summary = subtitle.text
        except NoSuchElementException:
            logging.warning("No subtitle description found")

        logging.info("Parsed outage: %s", outage)

        outages.append(outage)

    logging.info("Outages parsed")

    return outages
