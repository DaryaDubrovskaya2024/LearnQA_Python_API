import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data= self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_content = f"Users with email '{email}' already exists"
        assert response.content.decode('utf-8') == expected_content, f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_content = "Invalid email format"
        assert response.content.decode(
                'utf-8') == expected_content, f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('missing_field', [
        'username', 'password', 'firstName', 'lastName', 'email'
        ])
    def test_create_user_without_required_field(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_content = f"The following required params are missed: {missing_field}"
        assert response.content.decode(
            'utf-8') == expected_content, f"Unexpected response content {response.content}"

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_content = "The value of 'firstName' field is too short"
        assert response.content.decode(
            'utf-8') == expected_content, f"Unexpected response content {response.content}"

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A' * 251

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_content = "The value of 'firstName' field is too long"
        assert response.content.decode('utf-8') == expected_content, f"Unexpected response content {response.content}"



