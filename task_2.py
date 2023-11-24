import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver():
    # создаем драйвер для Google Chrome
    driver = webdriver.Chrome()
    driver.get("http://149.255.118.78:7080")

    # используем для закрытия браузера
    yield driver
    driver.close()

# проверка валидных данных для входа
def test_true_auth(driver):
    login_field = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "loginEmail")))
    login_field.send_keys("test@protei.ru")

    password_field = driver.find_element(by=By.ID, value="loginPassword")
    password_field.send_keys("test")

    enter_button = driver.find_element(by=By.CSS_SELECTOR, value=".uk-button")
    enter_button.click()

    main_title = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "h3")))

    assert main_title.is_displayed()
    assert main_title.text == "Добро пожаловать!"

# проверка авторизации с вызовом сообщения "Неверный формат Email"
def test_invalid_email_format_auth(driver):
    login_field = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "loginEmail")))
    login_field.send_keys("1")

    enter_button = driver.find_element(by=By.CSS_SELECTOR, value=".uk-button")
    enter_button.click()

    message = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "p")))

    assert message.is_displayed()
    assert message.text == "Неверный формат E-Mail"


# проверка авторизации с вызовом сообщения "Неверный Email или пароль"
def test_invalid_email_or_pass_auth(driver):
    login_field = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "loginEmail")))
    login_field.send_keys("student@protei.ru") #используем действующий email

    enter_button = driver.find_element(by=By.CSS_SELECTOR, value=".uk-button")
    enter_button.click()

    message = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-alert.uk-alert-danger")))

    assert message.is_displayed()
    assert message.text == "Неверный E-Mail или пароль"
