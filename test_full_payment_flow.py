import os, random, hashlib, argparse, json, time
import requests
import undetected_chromedriver as uc
from pages.Page import *
from pages.AmountInputPage import *
from pages.WalletConnectPage import *
from dotenv import load_dotenv
load_dotenv()

amount_input_page = AmountInputPage()
wallet_connect_page = WalletConnectPage()

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
    if (fiat_type != ""):
        data['amount_type'] = fiat_type
    if (uimode == 'switchable'):
        data['uimode'] = 'switchable'
        r = requests.post(url = request_url, data = data)
        payment_url = json.loads(r.text)['url'] + '/ww'
    else:
        r = requests.post(url = request_url, data = data)
        payment_url = json.loads(r.text)['url']

    return payment_url

def open_new_tab_and_close_current_tab(driver):
    driver.switch_to.new_window('tab')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def run_test_amount_set_by_payer(driver, env, amounts, uimode):
    print('Testing payer input fiat amount - ' + uimode +' UI mode')
    for item in amounts:
        print('Testing amount: ' + item['amount'])
        payment_url = get_payment_url(env, item['amount'], item['amount_type'], uimode)
        time.sleep(2)
        driver.get(payment_url)
        amount_input_page.run_test(driver, item['amount'])
        wallet_connect_page.run_test(driver, item['amount'], item['amount_type'])
        open_new_tab_and_close_current_tab(driver)

def run_test_amount_set_by_merchant(driver, env, amounts, uimode):
    print('Testing merchant input fiat amount - ' + uimode +' UI mode')
    for item in amounts:
        print('Testing amount: ' + item['amount'])
        payment_url = get_payment_url(env, item['amount'], item['amount_type'], uimode)
        time.sleep(2)
        driver.get(payment_url)
        wallet_connect_page.run_test(driver, item['amount'], item['amount_type'])
        open_new_tab_and_close_current_tab(driver)

def main():
    parser = argparse.ArgumentParser("args")
    parser.add_argument("--env", dest='env', help="Enter environment name", type=str)
    parser.add_argument("--amounts", dest='amounts', help="Enter amounts config file PATH", type=str)
    parser.add_argument("--by", dest='by', help="Enter whom sets payment amounts ('payer' or 'merchant')", type=str)
    args = parser.parse_args()
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    amounts_config = json.load(open(os.path.join(__location__,args.amounts)))

    driver = uc.Chrome(version_main=112)

    if (args.by == 'payer'):  #Test payer input fiat amount
        run_test_amount_set_by_payer(driver, args.env, amounts_config, 'basic')
        run_test_amount_set_by_payer(driver, args.env, amounts_config, 'switchable')
        driver.quit()
    else:   #Test merchant input fiat amount
        run_test_amount_set_by_merchant(driver, args.env, amounts_config, 'basic')
        run_test_amount_set_by_merchant(driver, args.env, amounts_config, 'switchable')
        driver.quit()

main()