import time
from random import choice
from string import ascii_letters

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        self.user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Сhanged Name"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    # Попытаемся изменить данные пользователя, будучи неавторизованными.
    def test_edit_user_being_unauthorized(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_first_name = "New Name"
        data = {"firstName": new_first_name}
        response = MyRequests.put(f"/user/{user_id}", data=data)
        print(response.content)
        assert "Auth token not supplied" in response.content.decode(), "Внимание! Полученный ответ не соответствует целевому!"

    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_being_authorized_by_other(self):
        # Регистрируем первого пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        # Ждем 2 секунды, чтобы не совпали при генерации emails первого и второго пользователей и регистрируем второго пользователя.
        time.sleep(2)
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        # ASSERT - Проверяем, что оба пользователя созданы успешно.
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        # Наполняем переменные данными.
        id_of_the_first_user = self.get_json_value(response1, "id")
        id_of_second_user = self.get_json_value(response2, "id")
        email_2 = register_data2['email']
        password_2 = register_data2['password']

        # LOGIN - авторизуемся под вторым пользователем
        login_data = {
            'email': email_2,
            'password': password_2
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid_of_second_user = self.get_cookie(response2, "auth_sid")
        token_of_second_user = self.get_header(response2, "x-csrf-token")
        print(response2.content)

        # EDIT - Пытаемся изменить данные первого пользователя, будучи авторизованными под вторым.
        new_username = "NewUserName"
        data = {"username": new_username}
        response = MyRequests.put(f"/user/{id_of_the_first_user}", data=data,
                                  headers={"x-csrf-token": token_of_second_user},
                                  cookies={"auth_sid": auth_sid_of_second_user})
        print(response.request.body)
        assert "" in response.content.decode(), "Внимание! Полученный ответ не соответствует целевому!"

        # Проверяем у какого из пользователей изменились данные!
        response1 = MyRequests.get(f"/user/{id_of_the_first_user}")
        response2 = MyRequests.get(f"/user/{id_of_second_user}")
        Assertions.assert_json_value_by_name(response1, "username", "learnqa",
                                             f"Полученное имя пользователя отличается от целевого {new_username}")
        Assertions.assert_json_value_by_name(response2, "username", "NewUserName",
                                             f"Полученное имя пользователя отличается от целевого {new_username}")

    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @.
    def test_edit_user_without_at(self):
        # REGISTER - создаем нового пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        # LOGIN - авторизуемся в системе
        email = register_data['email']
        password = register_data['password']
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        print(response2.content)

        # EDIT - пробуем изменить email на новый без "@"
        new_email = "vinkotovexample.com"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )
        print(response3.content)
        Assertions.assert_code_status(response3, 400), "Внимание! Реакция сервера отличается от целевой."

        # CHECK IN - проверяем, что после попытки изменить email, он остался прежним.
        response1 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response1, "email", f"{email}",
                                             f"Полученный адрес отличается от целевого {email}")

    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_firstname_to_short_value(self):
        # REGISTER - создаем нового пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        # LOGIN - авторизуемся в системе
        email = register_data['email']
        password = register_data['password']
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT - пробуем изменить firstName на новый
        first_name = ''.join(choice(ascii_letters) for i in range(1))

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": first_name}
                                   )
        print(response3.content)
        Assertions.assert_code_status(response3, 400), "Внимание, код ответа сервера подозрительно отличается от 400!"
        Assertions.assert_json_value_by_name(response3, "error", f"Too short value for field firstName",
                                             f"Полученный ответ отличается от ожидаемого: 'Too short value for field firstName'")

        # CHECK IN - проверяем, что после попытки изменить firsName, он остался прежним.
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        print(response4.content)
        Assertions.assert_json_value_by_name(response4, "firstName", f"{register_data['firstName']}",
                                             f"Полученный адрес отличается от целевого '{register_data['firstName']}'")
