import os, random, hashlib, argparse, json, time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
load_dotenv()

INPUT_PAYMENT_AMOUNTS = {
    "0.1": "0.10",
    "0.11": "0.11",
    "1": "1.00",
    "1.11" : "1.11",
    "10" : "10.00",
    "10.12" : "10.12",
    "100" : "100.00",
    "100.1" : "100.10",
    "1000" : "1000.00",
    "1000.12" : "1000.12",
    "10000" : "10000.00",
    "100000.1" : "100000.10",
}

def get_payment_url(env, amount_to_be_charged, uimode):
    payment_url = ''
    request_url = os.getenv(env + '_DOMAIN') + '/api/v1/payment/receive'
    auth_token = os.getenv(env + '_AUTH_TOKEN')
    hash_token = os.getenv(env + '_HASH_TOKEN')
    order_code = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    raw = '{}::{}::{}'.format(order_code, amount_to_be_charged, hash_token).encode('utf-8')
    verify_token = hashlib.sha256(raw).hexdigest()

    if (uimode == 'switchable'):
        if (amount_to_be_charged == ''):
            data = {
                'identification_token': auth_token,
                'order_code': order_code,
                'verify_token': verify_token,
                'uimode': 'switchable'
            }
        else:
            data = {
                'identification_token': auth_token,
                'order_code': order_code,
                'verify_token': verify_token,
                'amount': amount_to_be_charged,
                'uimode': 'switchable'
            }
        r = requests.post(url = request_url, data = data)
        payment_url = json.loads(r.text)['url'] + '/ww'
    else:
        if (amount_to_be_charged == ''):
            data = {
                'identification_token': auth_token,
                'order_code': order_code,
                'verify_token': verify_token,
            }
        else:
            data = {
                'identification_token': auth_token,
                'order_code': order_code,
                'verify_token': verify_token,
                'amount': amount_to_be_charged,
            }
        r = requests.post(url = request_url, data = data)
        payment_url = json.loads(r.text)['url']

    return payment_url

def enter_payment_amount(driver, amount):
    element = '//input[@class="price"]'
    WebDriverWait(driver, timeout=20).until(EC.visibility_of_element_located((By.XPATH, element))).send_keys(amount)
    # Click on PAY button
    element = '/html/body/div[1]/div/article/div/div[2]/div/div[2]/div[2]/div/div[3]/div/button'
    WebDriverWait(driver, timeout=20).until(EC.element_to_be_clickable((By.XPATH, element))).click()

def check_fiat_amount(driver, amount):
    element = '//p[@class="fiat undefined"]'
    WebDriverWait(driver, timeout=20).until(EC.presence_of_element_located((By.XPATH, element)))
    assert driver.find_element(By.XPATH, element).text.strip() == str(amount) + ' USD'


def test_payment_input_amount_page(driver, amount):
    enter_payment_amount(driver=driver, amount=amount)

def test_payment_wallet_connect_page(driver, amount):
    check_fiat_amount(driver=driver, amount=amount)

def main():
    parser = argparse.ArgumentParser("args")
    parser.add_argument("--env", dest='env', help="Enter environment name", type=str)
    parser.add_argument("--uimode", dest='uimode', help="Enter uimode", type=str)
    args = parser.parse_args()
    for amount in INPUT_PAYMENT_AMOUNTS:
        print('Testing amount: ' + amount)
        driver = uc.Chrome(version_main=112)
        payment_url = get_payment_url(args.env, '', args.uimode)
        driver.get(payment_url)
        test_payment_input_amount_page(driver, amount)
        test_payment_wallet_connect_page(driver, INPUT_PAYMENT_AMOUNTS[amount])
        time.sleep(3)
        driver.refresh()
        test_payment_wallet_connect_page(driver, INPUT_PAYMENT_AMOUNTS[amount])
        time.sleep(3)
        driver.quit()

main()