from .test_setup import UserTestSetUp, MissingPersonTestSetUp
from rest_framework import status
from django.http import JsonResponse


class UserTestViews(UserTestSetUp):

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

    def test_user_end_point(self):
        user_response = self.client.get(self.user_url)
        user_response_content = self.byteToDict(user_response.content)
        self.assertEqual(user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_response_content['user'], self.register_data['username'])


class MissingPersonTestViews(MissingPersonTestSetUp):

    def test_add_missing_person_correctly(self):
        add_missing_res_content = self.byteToDict(self.add_missing_responses[0].content)
        self.assertEqual(add_missing_res_content['name'], self.missing_person_data[0]["name"])
        self.assertEqual(self.add_missing_responses[0].status_code, status.HTTP_201_CREATED)
        self.assertEqual(add_missing_res_content['reported_by']['user'], self.register_data['username'])

    def test_get_missing_people(self):
        get_missing_people_response = self.client.get(self.missing_person_url)
        get_missing_people_response_content = self.byteToDict(get_missing_people_response.content)
        self.assertEqual(len(get_missing_people_response_content), len(self.missing_person_data))
        self.assertEqual(get_missing_people_response.status_code, status.HTTP_200_OK)
        for index in range(len(get_missing_people_response_content)):
            self.assertEqual(get_missing_people_response_content[index]['name'], self.missing_person_data[index]["name"])
            self.assertEqual(get_missing_people_response_content[index]['reported_by']['user'], self.register_data['username'])

    def test_get_missing_person_by_id_correctly(self):
        get_missing_person_response = self.client.get(self.missing_person_url+"/1")
        get_missing_person_response_content = self.byteToDict(get_missing_person_response.content)
        self.assertEqual(get_missing_person_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_missing_person_response_content['name'], self.missing_person_data[0]["name"])
        self.assertEqual(get_missing_person_response_content['reported_by']['user'], self.register_data['username'])

    def test_get_missing_person_by_invalid_id(self):
        get_missing_person_response = self.client.get(self.missing_person_url+"/6")
        get_missing_person_response_content = self.byteToDict(get_missing_person_response.content)
        self.assertEqual(get_missing_person_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_missing_person_response_content['message'], 'User Does not exist')

    def test_patch_name_missing_person_by_id(self):
        get_missing_person_response = self.client.get(self.missing_person_url+"/1")
        get_missing_person_response_content = self.byteToDict(get_missing_person_response.content)
        with open(f'images/c1.jpg', 'rb') as img:
            patch_data = {'image': img, 'name': self.fake.email().split("@")[0]}
            patch_missing_person_response = self.client.patch(self.missing_person_url+"/1",patch_data,format='multipart')
        patch_missing_person_response_content = self.byteToDict(patch_missing_person_response.content)
        self.assertEqual(patch_missing_person_response.status_code, status.HTTP_202_ACCEPTED)
        self.assertNotEqual(get_missing_person_response_content['name'], patch_missing_person_response_content['name'])
        self.assertEqual(get_missing_person_response_content['id'], patch_missing_person_response_content['id'])

    def test_delete_missing_person_by_id(self):
        get_missing_person_response_before_deleting = self.client.get(self.missing_person_url+"/1")
        self.assertEqual(get_missing_person_response_before_deleting.status_code, status.HTTP_200_OK)

        delete_missing_person_response = self.client.delete(self.missing_person_url+"/1")
        delete_missing_person_response_content = self.byteToDict(delete_missing_person_response.content)
        self.assertEqual(delete_missing_person_response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(delete_missing_person_response_content['message'], 'deleted')

        get_missing_person_response_after_deleting = self.client.get(self.missing_person_url+"/1")
        self.assertEqual(get_missing_person_response_after_deleting.status_code, status.HTTP_404_NOT_FOUND)

        delete_non_existing_missing_person_response = self.client.delete(self.missing_person_url+"/6")
        delete_non_existing_missing_person_response_content = self.byteToDict(delete_non_existing_missing_person_response.content)
        self.assertEqual(delete_non_existing_missing_person_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete_non_existing_missing_person_response_content['message'], 'User Does not exist')

    def test_profile_end_point(self):
        profile_response = self.client.get(self.profile_url)
        profile_response_content = self.byteToDict(profile_response.content)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response_content[0]['reported_by']['user'], self.register_data['username'])
        self.assertEqual(profile_response_content[0]['name'], self.missing_person_data[0]['name'])

