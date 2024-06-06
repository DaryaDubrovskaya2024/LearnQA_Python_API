import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
payload = {"method": ["POST", "GET", "PUT", "DELETE"]}
http_invalid = {"http_method": ["OPTIONS", "HEAD", "PATCH"]}

#Делает http-запрос любого типа без параметра method

without_method = requests.request('payload', url)
print('Ответ на 1 вопрос')
print(f" Status code: {without_method.status_code}, Ответ:{without_method.text}")

#Делает http-запрос не из списка
response = requests.request('http_invalid', url)
print('Ответ на 2 вопрос')
print(f" Status code: {response.status_code}, Ответ:{response.text}")

#Делает запрос с правильным значением method

method = 'POST'
response_http_method = requests.request('POST', url, data={"method": method})
print('Ответ на 3 вопрос')
print(f" Status code: {response_http_method.status_code}, Ответ:{response_http_method.text}")

# Проверка всех возможных сочетаний
print('Ответ на 4 вопрос')

for method in payload["method"]:

    response_post = requests.post(url, data={"method": method})
    print(f"POST-запрос: Параметр: {method}, Status code: {response_post.status_code}, Ответ:{response_post.text}")
    response_get = requests.get(url, data={"method": method})
    print(f"GET-запрос Параметр: {method}, Status code: {response_get.status_code}, Ответ:{response_get.text}")
    response_put = requests.put(url, data={"method": method})
    print(f"PUT-запрос Параметр: {method}, Status code: {response_put.status_code}, Ответ:{response_put.text}")
    response_delete = requests.delete(url, data={"method": method})
    print(f"DELETE-запрос Параметр: {method}, Status code: {response_delete.status_code}, Ответ:{response_delete.text}")



