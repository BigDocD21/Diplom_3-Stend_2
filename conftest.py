import os
import secrets
import uuid

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.ingredient_modal import IngredientModal
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="both",
        choices=("chrome", "firefox", "both"),
        help="Браузер для UI-тестов: chrome, firefox или both",
    )


def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        selected = metafunc.config.getoption("browser")
        browsers = ["chrome", "firefox"] if selected == "both" else [selected]
        metafunc.parametrize("driver", browsers, indirect=True)


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get(
        "STELLAR_BASE_URL", "https://qa-stellarburgers.education-services.ru"
    ).rstrip("/")


@pytest.fixture
def driver(request, base_url):
    if request.param == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        browser = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        browser = webdriver.Firefox(options=options)

    try:
        browser.set_page_load_timeout(30)
        browser.get(base_url + "/")
        if request.param == "firefox":
            MainPage(browser, base_url).wait_for_constructor_ready()
            IngredientModal(browser, base_url).wait_for_modal_to_close()
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def user_data(base_url):
    email = os.environ.get("STELLAR_EMAIL")
    password = os.environ.get("STELLAR_PASSWORD")
    if email and password:
        yield {"email": email, "password": password}
        return

    user = {
        "email": f"test-{uuid.uuid4().hex}@example.org",
        "password": secrets.token_urlsafe(24),
        "name": "Тестовый пользователь",
    }
    try:
        response = requests.post(f"{base_url}/api/auth/register", json=user, timeout=30)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        pytest.fail(f"Не удалось создать временного пользователя: {exc}", pytrace=False)
    token = data.get("accessToken")
    if not data.get("success") or not token:
        pytest.fail("Сайт не вернул токен временного пользователя.", pytrace=False)
    try:
        yield {"email": user["email"], "password": user["password"]}
    finally:
        try:
            response = requests.delete(
                f"{base_url}/api/auth/user",
                headers={"Authorization": token},
                timeout=30,
            )
            response.raise_for_status()
            if not response.json().get("success"):
                raise ValueError("сервер не подтвердил удаление")
        except (requests.RequestException, ValueError) as exc:
            pytest.fail(f"Не удалось удалить временного пользователя: {exc}", pytrace=False)


@pytest.fixture
def main_page(driver, base_url):
    return MainPage(driver, base_url)


@pytest.fixture
def ingredient_modal(driver, base_url):
    return IngredientModal(driver, base_url)


@pytest.fixture
def order_feed_page(driver, base_url):
    return OrderFeedPage(driver, base_url)


@pytest.fixture
def logged_in_main_page(user_data, driver, base_url):
    LoginPage(driver, base_url).login(user_data["email"], user_data["password"])
    return MainPage(driver, base_url)
