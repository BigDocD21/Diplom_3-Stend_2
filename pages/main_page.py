import re

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.main_locators import MainLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.constructor_wait = WebDriverWait(
            driver, 30, ignored_exceptions=(StaleElementReferenceException,)
        )

    @allure.step("Переход на вкладку «Конструктор»")
    def go_to_constructor(self):
        self.click_element(MainLocators.TAB_CONSTRUCTOR)
        self.wait.until(EC.visibility_of_element_located(MainLocators.CONSTRUCTOR_HEADER))

    @allure.step("Переход на вкладку «Лента заказов»")
    def go_to_feed(self):
        self.click_element(MainLocators.TAB_FEED)
        self.wait.until(EC.visibility_of_element_located(MainLocators.FEED_HEADER))

    @allure.step("Получение списка карточек ингредиентов")
    def get_ingredient_cards(self):
        return self.find_elements(MainLocators.INGREDIENT_CARD)

    def _ingredient_card(self, index):
        cards = self.get_ingredient_cards()
        if index < 0 or index >= len(cards):
            raise IndexError(
                f"Недостаточно карточек ингредиентов: индекс {index}, доступно {len(cards)}"
            )
        return cards[index]

    def _ready_ingredient(self, driver, index):
        if any(element.is_displayed() for element in driver.find_elements(*MainLocators.LOADING_INDICATOR)):
            return False

        cards = driver.find_elements(*MainLocators.INGREDIENT_CARD)
        if index < 0 or index >= len(cards):
            return False

        card = cards[index]
        target = driver.find_element(*MainLocators.CONSTRUCTOR_DROP_AREA)
        if not card.is_displayed() or not target.is_displayed():
            return False

        image = card.find_element(*MainLocators.INGREDIENT_IMAGE)
        if not image.get_property("complete"):
            return False

        text = card.find_element(*MainLocators.INGREDIENT_COUNTER).text.strip()
        return (card, int(text)) if text.isdigit() else False

    @allure.step("Ожидание загрузки конструктора и ингредиента")
    def wait_for_constructor_ready(self, index=0):
        if index < 0:
            raise ValueError("Индекс ингредиента не может быть отрицательным")
        return self.constructor_wait.until(
            lambda driver: self._ready_ingredient(driver, index),
            "Не удалось дождаться готовности конструктора и ингредиента за 30 секунд",
        )

    @allure.step("Открытие карточки ингредиента")
    def click_ingredient_card(self, index=0):
        self.click_element_on_card(self._ingredient_card(index))

    @allure.step("Перетаскивание ингредиента в конструктор")
    def add_ingredient_via_drag_and_drop(self, index=0):
        card, _ = self.wait_for_constructor_ready(index)
        self.drag_and_drop_element(card, MainLocators.CONSTRUCTOR_DROP_AREA)

    @allure.step("Клик по кнопке «Оформить заказ»")
    def click_order_button(self):
        self.click_element(MainLocators.ORDER_SUBMIT_BTN)

    @allure.step("Получение текста кнопки заказа")
    def get_order_button_text(self):
        return self.get_text(MainLocators.ORDER_SUBMIT_BTN)

    @allure.step("Получение значений счётчиков заказов")
    def get_counters(self):
        return (
            self._counter_value(MainLocators.COUNTER_ALL_TIME),
            self._counter_value(MainLocators.COUNTER_TODAY),
        )

    @staticmethod
    def _read_counter(driver, locator):
        text = driver.find_element(*locator).text
        digits = re.sub(r"\D", "", text)
        return (int(digits),) if digits else False

    def _counter_value(self, locator):
        return self.wait.until(lambda driver: self._read_counter(driver, locator))[0]

    @allure.step("Ожидание увеличения счётчика заказов")
    def wait_for_order_counter_increase(self, locator, previous_value):
        def counter_increased(driver):
            result = self._read_counter(driver, locator)
            return result[0] if result and result[0] > previous_value else False

        return self.wait.until(counter_increased)

    @allure.step("Клик по карточке ингредиента")
    def click_element_on_card(self, element):
        if not self.is_visible_element(element):
            raise TimeoutException("Карточка ингредиента не стала доступна для клика")
        element.click()

    @allure.step("Проверка видимости конструктора")
    def is_constructor_visible(self):
        return self.is_visible(MainLocators.CONSTRUCTOR_HEADER)

    @allure.step("Проверка видимости кнопки «Оформить заказ»")
    def is_order_button_visible(self):
        return self.is_visible(MainLocators.ORDER_SUBMIT_BTN)

    @allure.step("Получение счётчика выбранного ингредиента")
    def get_ingredient_counter_value(self, index=0):
        _, counter = self.wait_for_constructor_ready(index)
        return counter

    @allure.step("Ожидание увеличения счётчика ингредиента")
    def wait_for_ingredient_counter_increase(self, previous_value, index=0):
        def counter_increased(driver):
            ingredient = self._ready_ingredient(driver, index)
            if not ingredient:
                return False
            _, value = ingredient
            return value if value > previous_value else False

        return self.constructor_wait.until(
            counter_increased,
            "Счётчик ингредиента не увеличился за 30 секунд после перетаскивания",
        )


    @allure.step("Ждать увеличения счётчика «Выполнено за всё время»")
    def wait_for_all_time_counter_increase(self, previous_value):
        return self.wait_for_order_counter_increase(MainLocators.COUNTER_ALL_TIME, previous_value)

    @allure.step("Ждать увеличения счётчика «Выполнено за сегодня»")
    def wait_for_today_counter_increase(self, previous_value):
        return self.wait_for_order_counter_increase(MainLocators.COUNTER_TODAY, previous_value)
