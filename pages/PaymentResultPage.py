from pages.Page import *
class PaymentResultPage(Page):

    def __init__(self):
        super().__init__()

    def run_test(self):
        pass

    def is_blockchain_processing(self, driver):
        # "Waiting for transaction result" element
        element = '/html/body/div[1]/div/article/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/p[1]/span'
        desired_display_result = 'Waiting for transaction result'
        WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, element)))
        return driver.find_element(By.XPATH, element).text.strip() == desired_display_result

    def is_payment_success(self, driver):
        # "Waiting for transaction result" element
        element = '//span[normalize-space()="Transaction Submitted"]'
        try:
            WebDriverWait(driver, timeout=40).until(EC.visibility_of_element_located((By.XPATH, element)))
            return True
        except:
            return False
    
    def is_payment_fail(self, driver):
        # "Waiting for transaction result" element
        element = '//span[normalize-space()="Invalid Transaction"]'
        try:
            WebDriverWait(driver, timeout=40).until(EC.visibility_of_element_located((By.XPATH, element)))
            return True
        except:
            return False