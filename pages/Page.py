from selenium.webdriver.remote.webdriver import By
from selenium.common.exceptions import WebDriverException
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
import pytest, time

class Page:
    def __init__(self):
        pass