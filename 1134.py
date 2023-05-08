import os, random, hashlib, argparse, json, time, pytest
import requests
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.common.exceptions import WebDriverException
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
load_dotenv()


MERCHANT_INPUT_FIAT_AMOUNTS = [
    #fiat amount is not displayed
    {
        "amount": "1",
        "amount_type": None,
        "fiat_display_result": ""
    },
    {
        "amount": "0.1",
        "amount_type": "USD",
        "fiat_display_result": "0.10 USD"
    },
    {
        "amount": "0.11",
        "amount_type": "USD",
        "fiat_display_result": "0.11 USD"
    },
    {
        "amount": "1",
        "amount_type": "USD",
        "fiat_display_result": "1.00 USD"
    },
    {
        "amount": "1.11",
        "amount_type": "USD",
        "fiat_display_result": "1.11 USD"
    },
    {
        "amount": "10",
        "amount_type": "USD",
        "fiat_display_result": "10.00 USD"
    },
    {
        "amount": "10.12",
        "amount_type": "USD",
        "fiat_display_result": "10.12 USD"
    },
    {
        "amount": "100",
        "amount_type": "USD",
        "fiat_display_result": "100.00 USD"
    },
    {
        "amount": "100.1",
        "amount_type": "USD",
        "fiat_display_result": "100.10 USD"
    },
    {
        "amount": "1000",
        "amount_type": "USD",
        "fiat_display_result": "1000.00 USD"
    },
    {
        "amount": "1000.12",
        "amount_type": "USD",
        "fiat_display_result": "1000.12 USD"
    },
    {
        "amount": "10000",
        "amount_type": "USD",
        "fiat_display_result": "10000.00 USD"
    },
    {
        "amount": "100000.1",
        "amount_type": "USD",
        "fiat_display_result": "100000.10 USD"
    },
]

PAYER_INPUT_FIAT_AMOUNTS = [
    {
        "amount": "0.1",
        "amount_type": "USD",
        "fiat_display_result": "0.10 USD"
    },
    {
        "amount": "0.11",
        "amount_type": "USD",
        "fiat_display_result": "0.11 USD"
    },
    {
        "amount": "1",
        "amount_type": "USD",
        "fiat_display_result": "1.00 USD"
    },
    {
        "amount": "1.11",
        "amount_type": "USD",
        "fiat_display_result": "1.11 USD"
    },
    {
        "amount": "10",
        "amount_type": "USD",
        "fiat_display_result": "10.00 USD"
    },
    {
        "amount": "10.12",
        "amount_type": "USD",
        "fiat_display_result": "10.12 USD"
    },
    {
        "amount": "100",
        "amount_type": "USD",
        "fiat_display_result": "100.00 USD"
    },
    {
        "amount": "100.1",
        "amount_type": "USD",
        "fiat_display_result": "100.10 USD"
    },
    {
        "amount": "1000",
        "amount_type": "USD",
        "fiat_display_result": "1000.00 USD"
    },
    {
        "amount": "1000.12",
        "amount_type": "USD",
        "fiat_display_result": "1000.12 USD"
    },
    {
        "amount": "10000",
        "amount_type": "USD",
        "fiat_display_result": "10000.00 USD"
    },
    {
        "amount": "100000.1",
        "amount_type": "USD",
        "fiat_display_result": "100000.10 USD"
    }
]

def get_payment_url(env, amount_to_be_charged, fiat_type, uimode):
    payment_url = ''
    request_url = os.getenv(env + '_DOMAIN') + '/api/v1/payment/receive'
    auth_token = os.getenv(env + '_AUTH_TOKEN')
    hash_token = os.getenv(env + '_HASH_TOKEN')
    order_code = ''.join(random.choice('0123456789abcdefghikklmountwxxwcawocxsrepABCDEF') for i in range(16))
    raw = '{}::{}::{}'.format(order_code, amount_to_be_charged, hash_token).encode('utf-8')
    verify_token = hashlib.sha256(raw).hexdigest()

    data = {
                'identification_token': auth_token,
                'order_code': order_code,
                'verify_token': verify_token,
            }
    if (amount_to_be_charged != ''):
        data['amount'] = amount_to_be_charged
    if (fiat_type != None):
        data['amount_type'] = fiat_type
    if (uimode == 'switchable'):
        data['uimode'] = 'switchable'
        r = requests.post(url = request_url, data = data)
        payment_url = json.loads(r.text)['url'] + '/ww'
    else:
        r = requests.post(url = request_url, data = data)
        payment_url = json.loads(r.text)['url']

    return payment_url

def enter_payment_amount(driver, input_amount):
    element = '//input[@class="price"]'
    WebDriverWait(driver, timeout=20).until(EC.visibility_of_element_located((By.XPATH, element))).send_keys(input_amount)
    # Click on PAY button
    element = '/html/body/div[1]/div/article/div/div[2]/div/div[2]/div[2]/div/div[3]/div/button'
    WebDriverWait(driver, timeout=20).until(EC.element_to_be_clickable((By.XPATH, element))).click()

def check_fiat_amount(driver, fiat_display_result):
    element = '//p[@class="fiat undefined"]'
    if (fiat_display_result):
        WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, element)))
        assert driver.find_element(By.XPATH, element).text.strip() == fiat_display_result
    else:
        with pytest.raises(WebDriverException):
            WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, element)))


def test_payment_input_amount_page(driver, input_amount):
    enter_payment_amount(driver=driver, input_amount=input_amount)

def test_payment_wallet_connect_page(driver, fiat_display_result):
    check_fiat_amount(driver=driver, fiat_display_result=fiat_display_result)

def main():
    parser = argparse.ArgumentParser("args")
    parser.add_argument("--env", dest='env', help="Enter environment name", type=str)
    parser.add_argument("--uimode", dest='uimode', help="Enter uimode", type=str)
    args = parser.parse_args()

    #Test merchant input fiat amount
    print('Testing merchant input fiat amount')
    for item in MERCHANT_INPUT_FIAT_AMOUNTS:
        print('Testing amount: ' + item['amount'])
        driver = uc.Chrome(version_main=112)
        payment_url = get_payment_url(args.env, item['amount'], item['amount_type'], args.uimode)
        time.sleep(3)
        driver.get(payment_url)
        test_payment_wallet_connect_page(driver, item['fiat_display_result'])
        time.sleep(3)
        driver.refresh()
        test_payment_wallet_connect_page(driver, item['fiat_display_result'])
        time.sleep(3)
        driver.quit()

    #Test merchant input fiat amount
    print('Testing payer input fiat amount')
    for item in PAYER_INPUT_FIAT_AMOUNTS:
        print('Testing amount: ' + item['amount'])
        driver = uc.Chrome(version_main=112)
        payment_url = get_payment_url(args.env, '', None, args.uimode)
        time.sleep(3)
        driver.get(payment_url)
        test_payment_input_amount_page(driver, item['amount'])
        test_payment_wallet_connect_page(driver, item['fiat_display_result'])
        time.sleep(3)
        driver.refresh()
        test_payment_wallet_connect_page(driver, item['fiat_display_result'])
        time.sleep(3)
        driver.quit()

main()