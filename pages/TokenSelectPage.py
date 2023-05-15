from pages.Page import *
class TokenSelectPage(Page):

    def __init__(self):
        super().__init__()

    def ac_click_first_token(self, driver):
        #second token
        element = '/html/body/div[1]/div/article/div/div[2]/div/div[2]/div[2]/div/div[3]/div[2]/div/div/div[2]'
        WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, element))).click()

    def run_test(self, driver):
        self.ac_click_first_token(driver=driver)
