from pages.Page import *
class WalletConnectPage(Page):

    def __init__(self):
        super().__init__()

    def run_test(self, driver, fiat_amount, fiat_symbol):
        self.check_fiat_displaying(driver, fiat_amount, fiat_symbol)
        driver.refresh()
        self.check_fiat_displaying(driver, fiat_amount, fiat_symbol)

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
