from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):
    def test_delete_user_negative(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response_delete = MyRequests.delete(f"/user/2", cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_delete, 400)

    def test_delete_user_positive(self):
        user_id, email, password, original_first_name = self.register_new_user()

        new_name = "Changed name"

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response_delete = MyRequests.delete(f"/user/{user_id}", cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response_delete, 200)

        response_get_deleted_user = MyRequests.get(f"/user/{user_id}", cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response_get_deleted_user, 404)

    def test_delete_user_negative_other_user(self):

        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response_register, 200)

        login_data_user1 = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login_user1 = MyRequests.post("/user/login", data=login_data_user1)
        auth_sid_user1 = self.get_cookie(response_login_user1, "auth_sid")

        register_data_user2 = self.prepare_registration_data(email="another_user@example.com")
        response_register_user2 = MyRequests.post("/user/", data=register_data_user2)
        Assertions.assert_code_status(response_register_user2, 200)

        login_data_user2 = {
            'email': register_data_user2['email'],
            'password': register_data_user2['password']
        }
        response_login_user2 = MyRequests.post("/user/login", data=login_data_user2)
        auth_sid_user2 = self.get_cookie(response_login_user2, "auth_sid")


        user_id_user1 = self.get_json_value(response_register, "id")
        response_delete = MyRequests.delete(f"/user/{user_id_user1}", cookies={"auth_sid": auth_sid_user2})
        Assertions.assert_code_status(response_delete, 400)
