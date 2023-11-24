import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    # Инициализация WebDriver
    driver = webdriver.Chrome()
    yield driver
    # Закрытие браузера после завершения теста
    driver.quit()


class LoginPage:
    # Локаторы элементов на странице
    USERNAME_INPUT = (By.ID, 'loginEmail')
    PASSWORD_INPUT = (By.ID, 'loginPassword')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.uk-button')

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()


# проверка валидных данных для входа
def test_true_auth(driver):
    # Открытие страницы с формой авторизации
    driver.get("http://149.255.118.78:7080")

    # Создание объекта Page для страницы входа
    login_page = LoginPage(driver)

    # Ввод данных и авторизация
    login_page.login("test@protei.ru", "test")

    title = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "h3")))
    assert title.is_displayed()
    assert title.get_attribute("class") == "uk-card-title"
    assert title.text == "Добро пожаловать!"

# проверка авторизации с вызовом сообщения "Неверный формат Email"
def test_invalid_email_format_auth(driver):
    # Открытие страницы с формой авторизации
    driver.get("http://149.255.118.78:7080")

    # Создание объекта Page для страницы входа
    login_page = LoginPage(driver)

    # Ввод данных и авторизация
    login_page.login("111", "")

    message = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "p")))

    assert message.is_displayed()
    assert message.text == "Неверный формат E-Mail"

# проверка авторизации с вызовом сообщения "Неверный Email или пароль"
def test_invalid_email_or_pass_auth(driver):
    # Открытие страницы с формой авторизации
    driver.get("http://149.255.118.78:7080")

    # Создание объекта Page для страницы входа
    login_page = LoginPage(driver)

    # Ввод данных и авторизация
    login_page.login("student@protei.ru", "")
    message = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-alert.uk-alert-danger")))

    assert message.is_displayed()
    assert message.text == "Неверный E-Mail или пароль"

