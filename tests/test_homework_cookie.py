import requests

def test_homework_cookie():
    response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
    cookies = response.cookies

    for cookie in cookies:
        print(f'{cookie.name}: {cookie.value}')

    cookie_name = 'HomeWork'
    expected_value = 'hw_value'


    assert cookie_name in cookies, f"Cookie '{cookie_name}' isn't in the response"
    actual_value = cookies.get(cookie_name)
    assert actual_value == expected_value, f"Expected result '{expected_value}' doesn't correspond to the actual result '{actual_value}'"