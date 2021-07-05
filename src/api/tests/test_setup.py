from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
import ast


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.missing_person_url = reverse("missing")
        self.fake = Faker()
        self.register_data = {
            'username': self.fake.email().split('@')[0],
            'email': self.fake.email(),
            'password': self.fake.email().split('@')[0],
        }
        self.login_data = {
            "email": self.register_data["email"],
            "password": self.register_data["password"]
        }
        self.register_res = self.client.post(self.register_url, self.register_data)
        self.jwt_token = self.register_res.cookies['jwt'].value

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    @staticmethod
    def byteToDict(byte_str):
        dict_str = byte_str.decode("UTF-8")
        return ast.literal_eval(dict_str)
