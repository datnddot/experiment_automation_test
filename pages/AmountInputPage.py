from pages.Page import *
class AmountInputPage(Page):

    def __init__(self):
        super().__init__()

    def ac_enter_payment_amount(self, driver, input_amount):
        element = '//input[@class="price"]'
        WebDriverWait(driver, timeout=20).until(EC.visibility_of_element_located((By.XPATH, element))).send_keys(input_amount)
        # Click on PAY button
        element = '/html/body/div[1]/div/article/div/div[2]/div/div[2]/div[2]/div/div[3]/div/button'
        WebDriverWait(driver, timeout=20).until(EC.element_to_be_clickable((By.XPATH, element))).click()

    def run_test(self, driver, input_amount):
        self.ac_enter_payment_amount(driver=driver, input_amount=input_amount)
