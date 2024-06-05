import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

all_response = response.history
last_response = response

print("Все редиректы:")
for resp in all_response:
    print(resp.url)

print("Итоговый адрес:")
print(last_response.url)

