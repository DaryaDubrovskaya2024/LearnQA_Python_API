import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

#Получить токен и время заведения задачи
response = requests.get(url)
answer = response.json()
token, seconds = answer['token'], answer['seconds']
print("Задача создана. Токен:", token)

#Проверка статуса до готовности задачи
status_data = requests.get(url, params={'token': token}).json()
print("Статус:", status_data['status'])

#Ожидание
print(f"Время ожидания {seconds} секунд...")
time.sleep(seconds)

#Статус после создания задачи
status_data = requests.get(url, params={'token': token}).json()
result = status_data['result']

if status_data['status'] == "Job is ready" and 'result' in status_data and status_data['result']:
    print("Задача создана успешно")
    print("Результат выполнения задачи:", status_data['result'])
else:
    print("Задача не создана")