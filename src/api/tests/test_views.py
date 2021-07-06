from .test_setup import TestSetUp
from rest_framework import status
from django.http import JsonResponse


class UserTestViews(TestSetUp):

    def test_user_can_register_correctly(self):
        res_data = self.byteToDict(self.register_res.getvalue())
        self.assertEqual(res_data["user"], self.register_data["username"])
        self.assertEqual(self.register_res.status_code, status.HTTP_200_OK)

    def test_user_can_login_correctly(self):
        res = self.client.post(self.login_url, self.login_data)
        res_data = self.byteToDict(res.getvalue())
        self.assertEqual(res_data["user"], self.register_data["username"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_cannot_login_without_password(self):
        self.login_data['password'] = ""
        res = self.client.post(self.login_url, self.login_data)
        res_data = self.byteToDict(res.getvalue())
        self.assertEqual(res_data["message"], "Incorrect password!")
        # should be 403
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_cannot_login_without_email(self):
        self.login_data['email'] = ""
        res = self.client.post(self.login_url, self.login_data)
        res_data = self.byteToDict(res.getvalue())
        self.assertEqual(res_data["message"], "User not found!")
        # should be 404
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_logout_correctly(self):
        request = JsonResponse({})
        request.set_cookie(key="jwt", value=self.jwt_token, httponly=True)
        logout_res = self.client.post(self.logout_url, request)
        self.assertEqual(logout_res.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_res.cookies['jwt'].value, '')
        self.assertEqual(logout_res.data['message'], 'success')


class MissingPersonTestViews(TestSetUp):

    def test_add_missing_person_correctly(self):
        with open('images/image.jpg', 'rb') as img:
            missing_person_name = self.fake.email().split("@")[0]
            data = {'image': img, 'name': missing_person_name}
            add_missing_response = self.client.post(self.missing_person_url, data, format='multipart')
            add_missing_res_content = self.byteToDict(add_missing_response.content)
            self.assertEqual(add_missing_res_content['name'], missing_person_name)
            self.assertEqual(add_missing_response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(add_missing_res_content['reported_by']['user'], self.register_data['username'])

