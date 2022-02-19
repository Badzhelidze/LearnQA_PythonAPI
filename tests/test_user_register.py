from datetime import datetime
from random import choice
from string import ascii_letters
import allure
import allure

from lib.my_requests import MyRequests
import pytest


from lib.assertions import Assertions
from lib.base_case import BaseCase


@allure.epic("Register cases")
@allure.story('Cases for testing register')
class TestUserRegister(BaseCase):
    email_data = [
        {'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'badzhelidze@mail.ru'},
        {'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'badzhelidze@mail.ru'},
        {'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'badzhelidze@mail.ru'},
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'badzhelidze@mail.ru'},
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa'}
    ]

    @allure.title("USER CREATION")
    @allure.description("Метод для создания пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("TRY CREATE USER WITH EXISTING EMAIL")
    @allure.description("Метод для попытки создания пользователя с уже существующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected content {response.content}"

    @allure.link('https://software-testing.ru/lms/mod/assign/view.php?id=244502')
    @allure.title("TRY CREATE USER WITH INCORRECT EMAIL")
    @allure.description("Создание пользователя с некорректным email - без символа '@'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_without_at(self):
        self.random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.wrong_email = f"learnqa{self.random_part}example.com"

        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.wrong_email
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected content {response.content}!!!"

    @allure.link('https://software-testing.ru/lms/mod/assign/view.php?id=244502')
    @allure.title("TRY CREATE USER WITHOUT ONE OF THE FIELDS")
    @allure.description("Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('data', email_data)
    def test_create_user_without_one_field(self, data):
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The following required params are missed" in response.content.decode(), "Внимание!Полученный ответ сервера не соответствует целевому!"
        print(response.request.body)

    @allure.link('https://software-testing.ru/lms/mod/assign/view.php?id=244502')
    @allure.title("CREATE USER WITH SHORT NAME")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Создание пользователя с очень коротким именем в один символ")
    def test_create_user_with_shortname(self):
        short_firstname = ''.join(choice(ascii_letters) for i in range(1))
        data = {
            'password': '123',
            'username': 'Ilya',
            'firstName': f'{short_firstname}',
            'lastName': 'learnqa',
            'email': 'badzhelidze@mail.ru'
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert "The value of 'firstName' field is too short" in response.content.decode(), "Внимание!Полученный ответ сервера не соответствует целевому!"
        print(response.content)


    @allure.link('https://software-testing.ru/lms/mod/assign/view.php?id=244502')
    @allure.title("CREATE USER WITH LONG NAME")
    @allure.testcase('https://software-testing.ru/lms/mod/assign/view.php?id=244502', 'CREATE USER WITH LONG NAME')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Создание пользователя с очень длинным именем - длиннее 250 символов")
    def test_create_user_with_longname(self):
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"learnqa{random_part}@example.com"
        firstname = ''.join(choice(ascii_letters) for i in range(251))
        data = {
            'password': '123',
            'username': 'Ilya',
            'firstName': f'{firstname}',
            'lastName': 'learnqa',
            'email': f'{email}'
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert "The value of 'firstName' field is too long" in response.content.decode(), "Внимание! Полученный ответ сервера не соответствует целевому!"
        print(response.content)