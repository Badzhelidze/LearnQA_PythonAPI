import requests


class Test_Cookie:
    def test_cookie_request(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(
            f'\n======> Метод GET "/homework_cookie" возвращает следующий набор HEADERS: '
            f'\n{dict(response.headers)} <=======, один из которых "x-secret-homework-header" равен: "{response.headers.get("x-secret-homework-header")}"')
        assert response.headers.get(
            "x-secret-homework-header") == "Some secret value", "Ошибка! МЫ не получаем нужный header  ='Some secret value'!"
