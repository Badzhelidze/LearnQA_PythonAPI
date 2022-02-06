import json
import time
import requests

# Script #1 - создаём задачу.
response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
content1 = json.loads(response1.content)
token = (content1["token"])
secs = (content1["seconds"])
payload = {"token": token}
print(response1.text)


# Script #2 - делаем один запрос с token ДО того, как задача готова. Убеждаемся в правильности поля status.
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)
content2 = json.loads(response2.content)
status = (content2["status"])
try:
    assert status == "Job is NOT ready"
    print(f'При запросе с token ДО того как задача готова получаем статус = "{status}"')
except AssertionError:
    print(f'!!!!Что-то пошло не так. Статус отличается от искомого "Job is NOT ready" и равен = {status} !!!!!')


# Script #3 - ждем нужное количество секунд.
print('                  ||')
print('                  ||')
print('                  \/')
print(f'Ждем нужное кол-во секунд: {secs} сек.')
time.sleep(secs)


# Script #4 - делаем один запрос c token ПОСЛЕ того, как задача готова. Убеждаемся в правильности поля status и наличии поля result.
response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)
content3 = json.loads(response3.content)
actual_status = (content3["status"])
result_field = (content3["result"])
try:
    assert actual_status == "Job is ready9"
    assert result_field is not None
    print(f'Получен статус = {actual_status}. Задача выполнена успешно!')
except AssertionError:
    print("Что-то пошло не так. Задача до сих пор в процессе выполнения!")