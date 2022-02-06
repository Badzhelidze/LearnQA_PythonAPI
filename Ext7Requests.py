import requests

# Задание №1
print("Задание №1: ")
response1_1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ сервера по заданию №1 для GET-запроса = " + response1_1.text)

response1_2 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ сервера по заданию №1 для POST-запроса = " + response1_2.text)

response1_3 = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ сервера по заданию №1 для PUT-запроса = " + response1_3.text)

response1_4 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ сервера по заданию №1 для DELETE-запроса = " + response1_4.text)

print("======================================================================")

# Задание №2
print("Задание №2: ")
response2_1 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ сервера по заданию №2 для HEAD-запроса = " + response2_1.text)

response2_2 = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ сервера по заданию №2 для PATCH-запроса = " + response2_2.text)

response2_3 = requests.options("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Ответ сервера по заданию №2 для OPTIONS-запроса = " + response2_3.text)
print("======================================================================")

# Задание №3
print("Задание №3: ")
# GET-запрос
get_param = {"method": "GET"}
get_response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=get_param)
print(get_response.text)

# POST-запрос
post_param = {"method": "POST"}
post_response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=post_param)
print(get_response.text)

# PUT-запрос
put_param = {"method": "PUT"}
put_response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=put_param)
print(get_response.text)

# DELETE-запрос
delete_param = {"method": "DELETE"}
delete_response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=delete_param)
print(delete_response.text)
print("======================================================================")

# Задание №4
print("Задание №4. Получаем  комбинации реальных типов запроса и значений параметров ")
methods = ["get", "post", "put", "delete"]
list_of_meth_params = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]

for i in methods:
        for param in list_of_meth_params:
                response4_1 = requests.request(i,"https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
                print(f"Метод {i} с параметром params={param} получает '{response4_1.text}'. Код ответа сервера {response4_1.status_code}.")
print("======================================================================")


# Задание №4 - Дополнение
print("Дополнение к заданию №4. Получаем все возможные комбинации методов и параметров ")
meth_lst = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]

for parameter in meth_lst:
        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=parameter)
        print(f" GET-метод с params={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")

        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", data=parameter)
        print(f" GET-метод с data={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")

        response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=parameter)
        print(f" POST-метод с data={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")

        response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params=parameter)
        print(f" POST-метод с params={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")

        response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=parameter)
        print(f" PUT -метод с data={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")

        response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", params=parameter)
        print(f" PUT-метод с params={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")

        response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=parameter)
        print(f" DELETE-метод с data={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")

        response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params=parameter)
        print(f" DELETE-метод с params={parameter} получает ==> {response.text}. Код ответа = {response.status_code}")