from pages.Page import *
class PaymentDetailPage(Page):

    def __init__(self):
        super().__init__()

    def run_test(self, driver):
        self._ac_click_pay(driver=driver)

    def _ac_click_pay(self, driver):
        element = '//span[normalize-space()="Pay"]'
        WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, element))).click()