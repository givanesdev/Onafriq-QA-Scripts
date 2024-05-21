import sys
import time
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


class OnafriqAPI:
    profile: FirefoxProfile
    options: Options
    service: Service
    driver: webdriver.Firefox

    def __init__(self):
        self.options = Options()
        self.service = Service()
       # self.profile = FirefoxProfile("/home/update/.cache/mozilla/firefox/n2x71vnp.omosh")
       # self.options.profile = self.profile
        self.driver = webdriver.Firefox(service=self.service, options=self.options)

    def login_action(self) -> bool:
        try:
            # open connection to login page
            self.driver.get("https://www.automationexercise.com/login")

            # retrieve email field, password field and login button
            email = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="login-email"]')
            password = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="login-password"]')
            login_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="login-button"]')

            # we fill in username and password
            email.send_keys("qat@mailinator.com")
            password.send_keys("123456")

            # we click login button
            login_btn.click()
            return True
        finally:
            return False

    def scan_items_action(self) -> bool:
        try:
            # open connection to home page
            self.driver.get("https://www.automationexercise.com")

            # retrieve email field, password field and login button
            results = self.driver.find_elements(By.CLASS_NAME, 'productinfo')

            items = {}

            # Print the titles and links of the first 5 results
            for result in results:
                n = result.find_element(By.TAG_NAME, 'p')
                p = result.find_element(By.TAG_NAME, 'h2')

                if len(n.text) == 0:
                    continue

                pr = p.text[4:]
                items[n.text] = int(pr)
                # print(f'Title: {item["name"]}\nPrice: {item["price"]}\n')

            sorted_dict = OrderedDict(sorted(items.items(), key=lambda item: item[1]))
            for k, v in sorted_dict.items():
                print(f'Title: {k}\nPrice: {v}\n')

            return True
        finally:
            return False
        # Wait for the results to load
        # driver.implicitly_wait(5)

    def remove_adds(self) -> bool:
        try:
            iframe = self.driver.find_element(By.ID, 'aswift_6')
            self.driver.execute_script("""
                            var iframe = arguments[0];
                            iframe.parentNode.removeChild(iframe);
                        """, iframe)
        except Exception as e:
            pass

        try:
            iframe = self.driver.find_element(By.ID, 'aswift_6_host')
            self.driver.execute_script("""
                            var iframe = arguments[0];
                            iframe.parentNode.removeChild(iframe);
                        """, iframe)
        except Exception as e:
            pass

        while 1:
            try:
                iframe = self.driver.find_element(By.CLASS_NAME, 'adsbygoogle-noablate')
                self.driver.execute_script("""
                                var iframe = arguments[0];
                                iframe.parentNode.removeChild(iframe);
                            """, iframe)
            except Exception as e:
                break

    def fill_cart(self):
        try:
            # open connection to home page
            self.driver.get("https://www.automationexercise.com")

            # find women's page
            women_btn = self.driver.find_element(By.CSS_SELECTOR, '[href="#Women"]')
            self.remove_adds()
            women_btn.click()

            # remove ads and iframes blocking the page

            # find top dress page
            top_btn = self.driver.find_element(By.CSS_SELECTOR, '[href="/category_products/2"]')
            self.remove_adds()
            top_btn.click()

            # find the dress item and click
            dress_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-product-id="8"]')
            self.remove_adds()
            dress_btn.click()
            time.sleep(5)

            # find card modal view cart
            modal = self.driver.find_element(By.ID, 'cartModal')
            top_btn = modal.find_element(By.CSS_SELECTOR, '[href="/view_cart"]')
            self.remove_adds()
            top_btn.click()
            time.sleep(5)

            # find check out button and click
            checkout_btn = self.driver.find_element(By.CLASS_NAME, 'check_out')
            checkout_btn.click()
            time.sleep(5)
            self.remove_adds()

            # fill in message comment
            comment_field = self.driver.find_element(By.CSS_SELECTOR, '[name="message"]')
            comment_field.send_keys("Order placed.")

            # find payment button and press
            top_btn = self.driver.find_element(By.CSS_SELECTOR, '[href="/payment"]')
            self.remove_adds()
            top_btn.click()
            time.sleep(5)

            # fill in payment form
            name = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="name-on-card"]')
            number = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="card-number"]')
            cvc = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="cvc"]')
            month = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="expiry-month"]')
            year = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="expiry-year"]')

            name.send_keys("Test Card")
            number.send_keys("4100 0000 0000")
            cvc.send_keys("123")
            month.send_keys("01")
            year.send_keys("1900")

            # find pay submit button and press
            pay_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-qa="pay-button"]')
            self.remove_adds()
            pay_btn.click()
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    try:
        api = OnafriqAPI()
        api.login_action()
        api.scan_items_action()
        api.fill_cart()
    except KeyboardInterrupt:
        sys.exit(0)
