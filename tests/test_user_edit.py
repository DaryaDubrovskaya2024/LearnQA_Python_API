from lib.my_requests import MyRequests
import json
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        user_id, email, password, original_first_name = self.register_new_user()

        new_name = "Changed name"

        #LOGIN
        login_data={
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )


    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_not_auth(self):

        user_id, email, password, original_first_name = self.register_new_user()

        new_name = "Changed name"


        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})


        Assertions.assert_code_status(response2, 400)  # Expecting Unauthorized status code



    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_auth_as_other_user(self):
        # Register first user
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id1 = self.get_json_value(response1, "id")

        # Register second user
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        user_id2 = self.get_json_value(response2, "id")
        email2 = register_data2['email']
        password2 = register_data2['password']

        # Login as second user
        login_data = {
            'email': email2,
            'password': password2
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        new_name = "Changed name"
        response4 = MyRequests.put(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response4, 400)


    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_email_invalid(self):
        user_id, email, password, original_first_name = self.register_new_user()

        new_name = "Changed name"

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_email = "invalidemailexample.com"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response3, 400)


    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_first_name_short(self):
        user_id, email, password, original_first_name = self.register_new_user()

        new_name = "Changed name"

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_first_name = "A"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )
        Assertions.assert_code_status(response3, 400)









