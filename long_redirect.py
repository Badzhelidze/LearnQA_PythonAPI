import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
#redirect_history = response.history
#final_url = response.url

print(response.history)
print(response.history[0].url)
print(response.history[1].url)
print(response.history[2].url)
print(response.history[3].url)

print(response.url)