import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from locators.main_locators import MainLocators
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    @allure.step("Получение заказов в разделе «В работе»")
    def get_work_orders_list(self):
        return self.driver.find_elements(*MainLocators.ORDERS_LIST)

    @allure.step("Получение первого номера заказа в разделе «В работе»")
    def get_first_order_number(self):
        for item in self.get_work_orders_list():
            text = item.text.strip()
            if text.isdigit():
                return text
        return None

    @allure.step("Ожидание номера заказа в разделе «В работе»")
    def check_order_exists_in_feed(self, expected_number):
        expected = int(expected_number)

        def order_is_present(_driver):
            try:
                for item in self.get_work_orders_list():
                    number = item.text.strip()
                    if number.isdigit() and int(number) == expected:
                        return True
            except StaleElementReferenceException:
                return False
            return False

        try:
            return self.wait.until(order_is_present)
        except TimeoutException:
            return False
