from selenium.webdriver.common.by import By

class MainLocators:

    TAB_CONSTRUCTOR = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and .//p[text()='Конструктор']]")
    TAB_FEED = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and .//p[text()='Лента Заказов']]")

    INGREDIENT_CARD = (By.XPATH, "//a[contains(@href, '/ingredient/')]")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "p[class*='counter_counter__num']")
    INGREDIENT_IMAGE = (By.CSS_SELECTOR, "img")
    LOADING_INDICATOR = (
        By.CSS_SELECTOR,
        '[class*="Modal_modal_opened__"] img[class*="Modal_modal__loading"]',
    )

    CONSTRUCTOR_DROP_AREA = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket__']")
    CONSTRUCTOR_HEADER = (By.XPATH, '//h1[normalize-space()="Соберите бургер"]')

    ORDER_SUBMIT_BTN = (By.XPATH, '//button[text()="Оформить заказ"]')

    COUNTER_ALL_TIME = (By.XPATH, '//p[text()="Выполнено за все время:"]/following-sibling::p')
    COUNTER_TODAY = (By.XPATH, '//p[text()="Выполнено за сегодня:"]/following-sibling::p')

    MODAL_WINDOW = (By.CSS_SELECTOR, '[class*="Modal_modal_opened__"]')
    MODAL_OVERLAY = (By.CSS_SELECTOR, '[class*="Modal_modal_overlay__"]')
    MODAL_CLOSE_BTN = (
        By.CSS_SELECTOR,
        '[class*="Modal_modal_opened__"] button[class*="Modal_modal__close"]',
    )
    ORDER_NUMBER = (
        By.CSS_SELECTOR,
        '[class*="Modal_modal_opened__"] [class*="Modal_modal__title_shadow__"]',
    )

    LOGIN_INPUT = (By.XPATH, '//form//label[normalize-space()="Email"]/following-sibling::input')
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_SUBMIT_BTN = (By.XPATH, '//form//button[normalize-space()="Войти"]')

    REG_NAME_INPUT = (By.XPATH, '//label[text()="Имя"]/following-sibling::input')
    REG_EMAIL_INPUT = (By.XPATH, '//label[text()="Email"]/following-sibling::input')
    REG_PASSWORD_INPUT = (By.XPATH, '//label[text()="Пароль"]/following-sibling::input')
    REG_REGISTER_BTN = (By.XPATH, '//button[text()="Зарегистрироваться"]')
    REG_LOGIN_BTN = (By.XPATH, '//button[text()="Войти"]')

    FEED_HEADER = (By.XPATH, '//h1[text()="Лента заказов"]')
    ORDERS_LIST = (By.XPATH, '//ul[contains(@class, "OrderFeed_orderListReady")]//li')
