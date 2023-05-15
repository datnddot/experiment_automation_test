from selenium.webdriver.remote.webdriver import By
from selenium.common.exceptions import WebDriverException
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time, os, sys
from dotenv import load_dotenv
load_dotenv()

class Metamask():
    def __init__(self):
        pass
    
    def unlock_and_connect(self, driver):
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        try:
            self._unlock(driver)
        except:
            pass
        try:
            self._next(driver)
        except:
            pass
        try:
            self._connect(driver)
        except:
            pass
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
    
    def sign(self, driver):
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        try:
            self._sign(driver)
        except:
            pass
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
    
    def confirm(self, driver, gasConfig=None):
        time.sleep(8)
        driver.switch_to.window(driver.window_handles[-1])
        if gasConfig:
            self._edit_gas(driver, gasConfig)
        time.sleep(3)
        # sys.stdin.read()
        element = '//button[normalize-space()="Confirm"]'
        # WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.XPATH, element)))
        # actions = ActionChains(driver)
        # actions.move_to_element(driver.find_element(By.XPATH,element)).perform()
        WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.XPATH, element))).click()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
    
    def _edit_gas(self, driver, gasAmount):
        element = '//button[@data-testid="edit-gas-fee-button"]'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).click()
        element = '//button[@data-testid="edit-gas-fee-item-custom"]'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).click()
        element = '//a[normalize-space()="Edit"]'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).click()
        element = '//input[@data-testid="gas-limit-input"]'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).clear()
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).send_keys(gasAmount)
        element = '//button[normalize-space()="Save"]'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).click()

    def _connect(self, driver):
        element = '//button[normalize-space()="Connect"]'
        WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.XPATH, element))).click()
    
    def _sign(self, driver):
        element = '//button[normalize-space()="Sign"]'
        WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.XPATH, element))).click()

    def _unlock(self, driver):
        element = '//input[@data-testid="unlock-password"]'
        WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.XPATH, element)))
        driver.find_element(By.XPATH, element).send_keys(os.getenv('METAMASK_PASSWORD'))
        element = '//button[normalize-space()="Unlock"]'
        WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.XPATH, element))).click()
    
    def _next(self, driver):
        element = '//button[normalize-space()="Next"]'
        WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.XPATH, element))).click()