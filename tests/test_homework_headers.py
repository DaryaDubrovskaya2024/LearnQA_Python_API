import requests

def test_homework_headers():
    response = requests.get('https://playground.learnqa.ru/api/homework_header')
    headers = response.headers

    print("Headers:", headers)

    expected_headers = {
        "x-secret-homework-header": "Some secret value"
    }

    for header_name, expected_value in expected_headers.items():
        assert header_name in headers, f"Header {header_name} isn't in the response"
        assert headers[header_name] == expected_value, f"Expected result {expected_value} doesn't correspond to the actual result {header_name}"

    print("All expected headers are present and correct.")