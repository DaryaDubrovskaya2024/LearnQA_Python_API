import json.decoder
from datetime import datetime
from requests import Response
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Can't fine cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Can't fine header with name {headers_name} in the last response"
        return response.headers[headers_name]
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response isn't in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa2',
            'lastName': 'learnqa2',
            'email': email
        }

    def register_new_user(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
        user_id = self.get_json_value(response, "id")
        return user_id, register_data['email'], register_data['password'], register_data['firstName']