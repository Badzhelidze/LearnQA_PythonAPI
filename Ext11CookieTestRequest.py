import requests


class Test_Cookie:
    def test_cookie_request(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie", cookies={"HomeWork": "12345"})
        print(
            f'Метод GET "/homework_cookie" возвращает COOKIE = {dict(response.cookies)}, значение которой = "{response.cookies.get("HomeWork")}"')
        assert response.cookies.get('HomeWork') == "hw_value", "Ошибка! МЫ не получаем нужную COOKIE ='hw_value'!"

