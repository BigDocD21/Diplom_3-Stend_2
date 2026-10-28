import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открытие страницы по относительному пути")
    def open_page(self, path):

        full_url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.driver.get(full_url)

    @allure.step("Поиск элемента по локатору")
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Поиск списка элементов по локатору")
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Клик по элементу (с ожиданием кликабельности)")
    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step("Перетаскивание элемента в целевую зону")
    def drag_and_drop_element(self, source_element, target_locator):
        target = self.wait.until(EC.visibility_of_element_located(target_locator))
        if self.driver.capabilities.get("browserName") == "firefox":
            self.driver.execute_async_script(
                """
                const [source, target, done] = arguments;
                const dataTransfer = new DataTransfer();
                const rect = target.getBoundingClientRect();
                const coords = {
                    clientX: rect.x + rect.width / 2,
                    clientY: rect.y + rect.height / 2,
                };
                const fire = (element, type, position) => element.dispatchEvent(
                    new DragEvent(type, {
                        bubbles: true, cancelable: true, dataTransfer, ...position,
                    })
                );
                fire(source, 'dragstart', {});
                // React DnD обрабатывает перемещение в следующем кадре.
                setTimeout(() => {
                    fire(target, 'dragenter', coords);
                    fire(target, 'dragover', coords);
                }, 100);
                setTimeout(() => {
                    fire(target, 'drop', coords);
                    fire(source, 'dragend', coords);
                    done();
                }, 250);
                """,
                source_element,
                target,
            )
            return
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_element, target).perform()

    @allure.step("Получение текста элемента")
    def get_text(self, locator):
        return self.find_element(locator).text

    @allure.step("Проверка видимости элемента по локатору")
    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    @allure.step("Проверка видимости переданного WebElement")
    def is_visible_element(self, element):
        try:
            self.wait.until(lambda d: element.is_displayed() and element.is_enabled())
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Ожидание исчезновения элемента по локатору")
    def wait_for_invisibility(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))
