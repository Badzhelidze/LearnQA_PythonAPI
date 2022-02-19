import time

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def setup(self):
        self.data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

    # NEGATIVE - Пытаемся удалить пользователя с ID = 2, будучи авторизованным под ним.
    def test_user_deleting_for_id(self):
        # AUTHORIZATION - авторизуемся под пользователем с ID = 2.
        response1 = MyRequests.post("/user/login", data=self.data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        # DELETE - удаляем пользователя по ID
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert "Please, do not delete test users with ID 1, 2, 3, 4 or 5." in response2.content.decode(), "Внимание! Попытка удаления могла завершиться успехом!"

        # CHECK IN  - Отправляем запрос на получение данных пользователя для проверки, что система не дала его удалить.
        response3 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        print(response3.content)
        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response3, expected_fields)

    # POSITIVE - Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
    def test_new_user_deleting(self):
        # Регистрируем нового пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        # ASSERT - Проверяем, что пользователь создан успешно.
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Наполняем переменные данными.
        user_id = self.get_json_value(response1, "id")
        email = register_data['email']
        password = register_data['password']

        # LOGIN - авторизуемся под созданным пользователем
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE - Пытаемся удалить созданного пользователя, будучи авторизованными под ним.
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        # CHECK IN  - Отправляем запрос на получение данных пользователя для проверки, что Система позволила его удалить.
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        print(response4.content)
        assert "User not found" in response4.content.decode(), f"Внимание! Обнаружен искомый ID = {user_id}, пользователь мог остаться в живых!"

    # NEGATIVE - попробовать удалить пользователя, будучи авторизованными под другим пользователем.
    def test_user_deleting_with_alien_id(self):
        # Регистрируем первого пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        # Ждем 2 секунды, чтобы не совпали при генерации email's первого и второго пользователей и регистрируем второго пользователя.
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

        # DELETE - Пытаемся удалить первого пользователя, будучи авторизованными под вторым.
        response_delete_first = MyRequests.delete(f"/user/{id_of_the_first_user}",
                                                  headers={"x-csrf-token": token_of_second_user},
                                                  cookies={"auth_sid": auth_sid_of_second_user})
        assert "" in response_delete_first.content.decode(), "Внимание! Полученный ответ не соответствует ожиданию!"

        # Проверяем какой из пользователей удалился.
        response1 = MyRequests.get(f"/user/{id_of_the_first_user}")
        response2 = MyRequests.get(f"/user/{id_of_second_user}")

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_code_status(response2, 404)
        assert "User not found" in response2.content.decode(), f"Внимание! Пользователь мог остаться в живых! Обратите внимание на ID = {id_of_second_user}"
