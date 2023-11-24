import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    # Инициализация WebDriver
    driver = webdriver.Chrome()
    yield driver
    # Закрытие браузера после завершения теста
    driver.quit()


class BasePage:
    def __init__(self, driver):
        self.driver = driver


# Класс для меню в шапке сайта
class MenuPage(BasePage):
    LOGIN_MENU = (By.ID, 'menuAuth')
    MAIN_MENU = (By.ID, 'menuMain')
    USER_MENU = (By.ID, 'menuUsersOpener')
    VARIANTS_MENU = (By.ID, 'menuMore')
    ADD_USER_MENU_BUTTON = (By.ID, 'menuUsersOpener')
    TABLE_MENU_BUTTON = (By.ID, 'menuUsers')
    ADD_USER_BUTTON = (By.ID, "menuUserAdd")

    # открыть страницу АВТОРИЗАЦИЯ
    def click_login_page(self):
        self.driver.find_element(*self.LOGIN_MENU).click()

    # открыть страницу ГЛАВНАЯ СТРАНИЦА
    def click_main_page(self):
        self.driver.find_element(*self.MAIN_MENU).click()

    # открыть страницу ПОЛЬЗОВАТЕЛИ
    def click_users_page(self):
        # Находим элемент меню "Пользователи"
        users_menu = self.driver.find_element(*self.ADD_USER_MENU_BUTTON)

        # Наводимся на пункт меню "Пользователи"
        ActionChains(self.driver).move_to_element(users_menu).perform()

        # Ждем, пока появится пункт "Добавить" и кликаем на него
        add_user_option = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.TABLE_MENU_BUTTON)
        )

        # Кликаем на "Добавление"
        add_user_option.click()

    # открыть страницу Добавление через меню в шапке сайта
    def click_add_user_from_menu(self):
        # Находим элемент меню "Пользователи"
        users_menu = self.driver.find_element(*self.ADD_USER_MENU_BUTTON)

        # Наводимся на пункт меню "Пользователи"
        ActionChains(self.driver).move_to_element(users_menu).perform()

        # Ждем, пока появится пункт "Добавить" и кликаем на него
        add_user_option = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.ADD_USER_BUTTON)
        )

        # Кликаем на "Добавление"
        add_user_option.click()

    # открыть страницу ВАРИАНТЫ
    def click_variants(self):
        self.driver.find_element(*self.VARIANTS_MENU).click()


# Класс для добавления нового пользователя
class AddUserPage(BasePage):
    EMAIL_FIELD = (By.ID, 'dataEmail')
    PASSWORD_FIELD = (By.ID, 'dataPassword')
    NAME_FIELD = (By.ID, 'dataName')
    GENDER_SELECT = (By.ID, 'dataGender')
    SELECT11 = (By.ID, 'dataSelect11')
    SELECT12 = (By.ID, 'dataSelect12')
    SELECT21 = (By.ID, 'dataSelect21')
    SELECT22 = (By.ID, 'dataSelect22')
    SELECT23 = (By.ID, 'dataSelect23')
    SEND_DATA_BUTTON = (By.ID, 'dataSend')

    def enter_email(self, email):
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def enter_name(self, name):
        self.driver.find_element(*self.NAME_FIELD).send_keys(name)

    def choose_gender(self, gender):
        gender_dropdown = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.GENDER_SELECT)
        )
        select = Select(gender_dropdown)
        select.select_by_visible_text(gender)

    def choose_select1(self, select1):
        self.driver.find_element(*self.SELECT11).click()
        if select1 == "11":
            self.driver.find_element(*self.SELECT11).click()
        else:
            self.driver.find_element(*self.SELECT12).click()

    def choose_select2(self, var21=None, var22=None, var23=None):
        self.driver.find_element(*self.SELECT21).click()  # так как при заходе на страницу уже стоит вариант 2.1

        if var21 is not None:
            self.driver.find_element(*self.SELECT21).click()
        if var22 is not None:
            self.driver.find_element(*self.SELECT22).click()
        if var23 is not None:
            self.driver.find_element(*self.SELECT23).click()

    def click_add_button(self):
        self.driver.find_element(*self.SEND_DATA_BUTTON).click()

    def registration(self, email, password, name, gender, var1, var21=None, var22=None, var23=None):
        self.enter_email(email)
        self.enter_password(password)
        self.enter_name(name)
        self.choose_gender(gender)
        self.choose_select1(var1)
        self.choose_select2(var21, var22, var23)
        self.click_add_button()


class LoginPage(BasePage):
    # Локаторы элементов на странице
    USERNAME_INPUT = (By.ID, 'loginEmail')
    PASSWORD_INPUT = (By.ID, 'loginPassword')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.uk-button')

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
    message = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-alert.uk-alert-danger")))
    assert message.is_displayed()
    assert message.text == "Неверный E-Mail или пароль"


# проверка добавления нового пользователя через ПОЛЬЗОВАТЕЛИ -> Добавление с валидными данными
def test_add_new_user(driver):
    test_true_auth(driver)
    # Создание объекта Page для страницы входа
    menu_page = MenuPage(driver)
    menu_page.click_add_user_from_menu()
    add_user_page = AddUserPage(driver)
    add_user_page.registration("student@protei.ru",
                               "student",
                               "testuser",
                               "Мужской",
                               "12",
                               "y",
                               None,
                               "y")
    title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-modal-body")))
    assert title.is_displayed()
    assert title.text == "Данные добавлены."


# проверка на ошибки в полях
def test_add_new_user_pairwise(driver):
    test_true_auth(driver)
    # Создание объекта Page для страницы входа
    menu_page = MenuPage(driver)
    menu_page.click_add_user_from_menu()
    add_user_page = AddUserPage(driver)

    # ошибка в почте
    add_user_page.registration("student@",
                               "student",
                               "testuser",
                               "Мужской",
                               "12",
                               "y",
                               None,
                               "y")
    message = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-alert.uk-alert-danger")))
    assert message.is_displayed()
    assert message.text == "Неверный формат E-Mail"

    driver.refresh()

    # ошибка в имени
    add_user_page.registration("student@protei.ru",
                               "student",
                               "",
                               "Мужской",
                               "12",
                               "y",
                               None,
                               "y")
    message = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-alert.uk-alert-danger")))
    assert message.is_displayed()
    assert message.text == "Поле Имя не может быть пустым"

    driver.refresh()

    # ошибка в пароле
    add_user_page.registration("student@protei.ru",
                               "",
                               "testuser",
                               "Мужской",
                               "12",
                               "y",
                               None,
                               "y")
    message = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-alert.uk-alert-danger")))
    assert message.is_displayed()
    assert message.text == "Поле Пароль не может быть пустым"

    driver.refresh()

# пример попарного тестирования (несколько строк)
def test_pairwise(driver):
    test_true_auth(driver)
    # Создание объекта Page для страницы входа
    menu_page = MenuPage(driver)
    menu_page.click_add_user_from_menu()
    add_user_page = AddUserPage(driver)

    add_user_page.registration("student1@protei.ru", "", "", "Мужской", "12", "y", "y", None)
    title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "uk-alert-danger")))
    # проверяем что появилось сообщение об ошибке
    assert title.is_displayed()

    driver.refresh()

    add_user_page.registration("student1@protei.ru", "", "Ivan", "Женский", "11", None, None, "y")
    title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "uk-alert-danger")))
    # проверяем что появилось сообщение об ошибке
    assert title.is_displayed()

    driver.refresh()

    add_user_page.registration("student12@protei.ru", "4343434", "", "Женский", "11", None, None, None)
    title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "uk-alert-danger")))
    # проверяем что появилось сообщение об ошибке
    assert title.is_displayed()


# проверка открытия страницы ВАРИАНТЫ
def test_open_variants(driver):
    test_true_auth(driver)
    # Создание объекта Page для страницы входа
    menu_page = MenuPage(driver)
    menu_page.click_variants()
    title = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "h3")))
    assert title.is_displayed()
    assert title.get_attribute("class") == "uk-card-title"
    assert title.text == "НТЦ ПРОТЕЙ"


# проверка открытия страницы ПОЛЬЗОВАТЕЛИ -> Таблица
def test_open_users(driver):
    test_true_auth(driver)
    # Создание объекта Page для страницы входа
    menu_page = MenuPage(driver)
    menu_page.click_users_page()
    usersPage = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "usersPage")))
    assert usersPage.is_displayed()


# проверка открытия страницы АВТОРИЗАЦИЯ -> Таблица
def test_open_login(driver):
    test_true_auth(driver)
    # Создание объекта Page для страницы входа
    menu_page = MenuPage(driver)
    menu_page.click_login_page()
    login_page = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "authPage")))
    assert login_page.is_displayed()
