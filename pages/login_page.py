import allure
from selenium.common.exceptions import ElementClickInterceptedException,StaleElementReferenceException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.main_locators import MainLocators
from pages.base_page import BasePage

class LoginPage(BasePage):

    LOGIN_PATH = "/login"

    def _submit_login_when_unobstructed(self):
        def click_submit(driver):
            button = driver.find_element(*MainLocators.LOGIN_SUBMIT_BTN)
            if not button.is_displayed() or not button.is_enabled():
                return False
            button.click()
            return True

        WebDriverWait(
            self.driver,
            30,
            ignored_exceptions=(
                ElementClickInterceptedException,
                StaleElementReferenceException,
            ),
        ).until(click_submit)

    @allure.step("Переход на страницу входа")
    def open_login_page(self):

        current_url = self.get_current_url()

        if self.LOGIN_PATH in current_url:
            return

        self.open_page(self.LOGIN_PATH)

    def login(self, email, password):
        with allure.step("Ввод данных и отправка формы входа"):
            self.open_login_page()
            email_field = self.find_element(MainLocators.LOGIN_INPUT)
            pass_field = self.find_element(MainLocators.PASSWORD_INPUT)
            email_field.clear()
            email_field.send_keys(email)
            pass_field.clear()
            pass_field.send_keys(password)
            self._submit_login_when_unobstructed()

            try:
                self.wait.until(EC.visibility_of_element_located(MainLocators.ORDER_SUBMIT_BTN))
            except TimeoutException as exc:
                raise TimeoutException(
                    "Не удалось подтвердить вход. Проверьте данные тестового пользователя "
                    "и доступность сайта."
                ) from exc
