from pages.Page import *
class WalletConnectPage(Page):

    def __init__(self):
        super().__init__()

    def run_test(self, driver, fiat_amount, fiat_symbol):
        self.check_fiat_displaying(driver, fiat_amount, fiat_symbol)
        driver.refresh()
        self.check_fiat_displaying(driver, fiat_amount, fiat_symbol)
        self.ac_click_metamask_button(driver)

    def ac_click_metamask_button(self, driver):
        element = '//span[normalize-space()="MetaMask"]'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).click()
    
    def ac_focus(self, driver):
        element = 'body'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.TAG_NAME, element))).click()

    def is_duplicate_payment_error(self, driver):
        element = '//span[normalize-space()="Payment cannot be continued due to the possibility of duplicate payment."]'
        desired_display_result = 'Payment cannot be continued due to the possibility of duplicate payment.'
        WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, element)))
        return driver.find_element(By.XPATH, element).text.strip() == desired_display_result

    def check_fiat_displaying(self, driver, fiat_amount, fiat_symbol):
        element = '//p[@class="fiat undefined"]'
        if (fiat_symbol):
            desired_fiat_display_result = "{:.2f}".format(float(fiat_amount)) + ' ' + fiat_symbol
            WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, element)))
            assert driver.find_element(By.XPATH, element).text.strip() == desired_fiat_display_result
        else:
            with pytest.raises(WebDriverException):
                WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, element)))
        time.sleep(1)
