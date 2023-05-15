import os, random, hashlib, argparse, json, time, sys
import requests
import undetected_chromedriver as uc
from pages.Page import *
from pages.AmountInputPage import *
from pages.WalletConnectPage import *
from pages.TokenSelectPage import *
from pages.PaymentDetailPage import *
from pages.PaymentResultPage import *
from plugins.Metamask import *
from dotenv import load_dotenv
load_dotenv()

amount_input_page = AmountInputPage()
wallet_connect_page = WalletConnectPage()
token_select_page = TokenSelectPage()
payment_detail_page = PaymentDetailPage()
payment_result_page = PaymentResultPage()
metamask = Metamask()

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



def run_test_payment_status_wallet_confirming(env, amounts, uimode):
    print('Testing merchant input fiat amount - ' + uimode +' UI mode')
    for item in amounts:
        print('Testing amount: ' + item['amount'])
        driver = uc.Chrome(user_data_dir='test_profile', version_main=112)
        # sys.stdin.read()
        payment_url = get_payment_url(env, item['amount'], item['amount_type'], uimode)
        time.sleep(2)
        driver.get(payment_url)
        time.sleep(2)
        driver.switch_to.new_window('tab')
        driver.get(payment_url)
        print(driver.window_handles)
        time.sleep(2)
        wallet_connect_page.ac_click_metamask_button(driver)
        metamask.unlock_and_connect(driver)
        token_select_page.run_test(driver)
        payment_detail_page.run_test(driver, False)
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[0])
        wallet_connect_page.ac_click_metamask_button(driver)
        assert wallet_connect_page.is_duplicate_payment_error(driver)
        driver.quit()

def run_test_payment_status_blockchain_processing(env, amounts, uimode):
    print('Testing merchant input fiat amount - ' + uimode +' UI mode')
    for item in amounts:
        print('Testing amount: ' + item['amount'])
        driver = uc.Chrome(user_data_dir='test_profile', version_main=112)
        # sys.stdin.read()
        payment_url = get_payment_url(env, item['amount'], item['amount_type'], uimode)
        time.sleep(2)
        driver.get(payment_url)
        time.sleep(2)
        driver.switch_to.new_window('tab')
        driver.get(payment_url)
        print(driver.window_handles)
        time.sleep(2)
        wallet_connect_page.ac_click_metamask_button(driver)
        metamask.unlock_and_connect(driver)
        time.sleep(3)
        token_select_page.run_test(driver)
        payment_detail_page.run_test(driver, True)
        time.sleep(3)
        if (payment_result_page.is_blockchain_processing(driver)):
            driver.switch_to.window(driver.window_handles[0])
            wallet_connect_page.ac_focus(driver)
            assert payment_result_page.is_blockchain_processing(driver)
        driver.quit()

def run_test_payment_status_success(env, amounts, uimode):
    print('Testing merchant input fiat amount - ' + uimode +' UI mode')
    for item in amounts:
        print('Testing amount: ' + item['amount'])
        driver = uc.Chrome(user_data_dir='test_profile', version_main=112)
        # sys.stdin.read()
        payment_url = get_payment_url(env, item['amount'], item['amount_type'], uimode)
        time.sleep(2)
        driver.get(payment_url)
        time.sleep(2)
        driver.switch_to.new_window('tab')
        driver.get(payment_url)
        print(driver.window_handles)
        time.sleep(2)
        wallet_connect_page.ac_click_metamask_button(driver)
        metamask.unlock_and_connect(driver)
        time.sleep(3)
        token_select_page.run_test(driver)
        payment_detail_page.run_test(driver, True)
        time.sleep(3)
        if (payment_result_page.is_payment_success(driver)):
            driver.switch_to.window(driver.window_handles[0])
            wallet_connect_page.ac_focus(driver)
            assert payment_result_page.is_payment_success(driver)
        time.sleep(3)
        driver.quit()

def run_test_payment_status_fail(env, amounts, uimode):
    print('Testing merchant input fiat amount - ' + uimode +' UI mode')
    for item in amounts:
        print('Testing amount: ' + item['amount'])
        driver = uc.Chrome(user_data_dir='test_profile', version_main=112)
        # sys.stdin.read()
        payment_url = get_payment_url(env, item['amount'], item['amount_type'], uimode)
        time.sleep(2)
        driver.get(payment_url)
        time.sleep(2)
        driver.switch_to.new_window('tab')
        driver.get(payment_url)
        print(driver.window_handles)
        time.sleep(2)
        wallet_connect_page.ac_click_metamask_button(driver)
        metamask.unlock_and_connect(driver)
        time.sleep(3)
        token_select_page.run_test(driver)
        payment_detail_page.run_test(driver)
        metamask.confirm(driver=driver, gasConfig=30000)
        time.sleep(3)
        if (payment_result_page.is_payment_fail(driver)):
            driver.switch_to.window(driver.window_handles[0])
            wallet_connect_page.ac_focus(driver)
            assert payment_result_page.is_payment_fail(driver)
        time.sleep(3)
        driver.quit()

def main():
    parser = argparse.ArgumentParser("args")
    parser.add_argument("--env", dest='env', help="Enter environment name", type=str)
    parser.add_argument("--amounts", dest='amounts', help="Enter amounts config file PATH", type=str)
    args = parser.parse_args()
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    amounts_config = json.load(open(os.path.join(__location__,args.amounts)))

    # run_test_payment_status_wallet_confirming(args.env, amounts_config, 'basic')
    # run_test_payment_status_wallet_confirming(args.env, amounts_config, 'switchable')

    # run_test_payment_status_blockchain_processing(args.env, amounts_config, 'basic')
    # run_test_payment_status_blockchain_processing(args.env, amounts_config, 'switchable')

    # run_test_payment_status_success(args.env, amounts_config, 'basic')
    # run_test_payment_status_success(args.env, amounts_config, 'switchable')

    run_test_payment_status_fail(args.env, amounts_config, 'basic')
    run_test_payment_status_fail(args.env, amounts_config, 'switchable')

main()