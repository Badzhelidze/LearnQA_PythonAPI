import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Getting cases")
@allure.story("Cases for testing USER information")
class TestUserGet(BaseCase):
    @allure.title("GET USER DATA")
    @allure.description("Получение данных о пользователе без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("Setup - метод для хранения credentials")
    def setup(self):
        self.data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

    @allure.title("GET USER INFORMATION AFTER AUTHORIZATION")
    @allure.description("Метод получения информации о пользователе после авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_auth_as_same_user(self):
        response1 = MyRequests.post("/user/login", data=self.data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.link('https://software-testing.ru/lms/mod/assign/view.php?id=244503')
    @allure.title("GET ALIEN USER INFORMATION WITH AUTHORIZATION BY FIRST")
    @allure.testcase('https://software-testing.ru/lms/mod/assign/view.php?id=244503',
                     'GET ALIEN USER INFORMATION WITH AUTHORIZATION BY FIRST')
    @allure.description(
        "Нужно написать тест, который авторизовывается одним пользователем, но получает данные другого (т.е. с другим ID). "
        "И убедиться, что в этом случае запрос также получает только username, так как мы не должны видеть остальные данные чужого пользователя.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_other_user(self):
        response1 = MyRequests.post("/user/login", data=self.data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_of_another_user = 1

        response2 = MyRequests.get(f"/user/{user_id_of_another_user}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        print(response2.content)
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")
