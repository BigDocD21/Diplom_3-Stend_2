import allure
import re
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from locators.main_locators import MainLocators
from pages.base_page import BasePage

class IngredientModal(BasePage):
    @allure.step("Проверка видимости модального окна с ингредиентом")
    def is_modal_open(self):
        return self.is_visible(MainLocators.MODAL_WINDOW)

    @allure.step("Получение заголовка модального окна")
    def get_modal_title(self):
        return self.get_text(MainLocators.MODAL_WINDOW)

    @allure.step("Получение деталей ингредиента")
    def get_ingredient_details(self):
        return self.get_text(MainLocators.MODAL_WINDOW)

    @allure.step("Ожидание номера оформленного заказа")
    def get_order_number(self):
        def visible_order_number(driver):
            if any(element.is_displayed() for element in driver.find_elements(*MainLocators.LOADING_INDICATOR)):
                return False
            for element in driver.find_elements(*MainLocators.ORDER_NUMBER):
                text = element.text.strip()
                if element.is_displayed() and re.fullmatch(r"\d+", text) and int(text) != 9999:
                    return text
            return False

        return WebDriverWait(self.driver, 40).until(
            visible_order_number
        )

    @allure.step("Закрытие модального окна кликом по крестику")
    def close_modal(self):
        self.click_element(MainLocators.MODAL_CLOSE_BTN)

    @allure.step("Ожидание полного закрытия модального окна")
    def wait_for_modal_to_close(self):
        def modal_and_overlay_hidden(driver):
            try:
                if any(element.is_displayed() for element in driver.find_elements(*MainLocators.MODAL_WINDOW)):
                    return False
                return driver.execute_script(
                    """
                    return !Array.from(document.querySelectorAll(arguments[0])).some(el => {
                        const style = getComputedStyle(el);
                        return style.visibility === 'visible' && style.pointerEvents !== 'none'
                            && Array.from(el.getClientRects()).some(rect => rect.width > 0 && rect.height > 0);
                    });
                    """,
                    MainLocators.MODAL_OVERLAY[1],
                )
            except StaleElementReferenceException:
                return False

        return self.wait.until(
            modal_and_overlay_hidden
        )
