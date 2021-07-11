import json
import time

import requests
from faker import Faker


class User:
    def __init__(self):
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
        self.jwt_token = ""

    def set_jwt_token(self,token):
        self.jwt_token = token


class MissingPerson:
    def __init__(self,image_index):
        self.fake = Faker()
        self.name = self.fake.email().split("@")[0]
        self.image_path = f'images/c{image_index}.jpg'


class TestSetUp:
    def __init__(self, host = "http://127.0.0.1:8000/api/"):
        self.register_url = host+'register'
        self.login_url = host+'login'
        self.logout_url = host+'logout'
        self.missing_person_url = host+"missing"
        self.user_url = host+'user'
        self.profile_url = host+'profile'
        self.find_url = host+"find"
        self.result_url = host + "result"
    def register_user(self,user):
        register_res = requests.post(self.register_url, json=user.register_data)
        user.set_jwt_token(register_res.cookies['jwt'])
        return register_res

    def login_user(self,user):
        login_res = requests.post(self.login_url, json=user.login_data)
        user.set_jwt_token(login_res.cookies['jwt'])
        return login_res

    def logout_user(self,user):
        logout_res = requests.post(self.logout_url, cookies={'jwt': user.jwt_token})

    def add_missing_person(self,user,missing_person):
        with open(missing_person.image_path, 'rb') as img:
            missing_res = requests.post(self.missing_person_url,data={'name': missing_person.name}, files={'image': img}, cookies={'jwt': user.jwt_token})
        return missing_res

    def get_all_missing_people(self):
        get_missing_res = requests.get(self.missing_person_url)
        return json.loads(get_missing_res.content.decode())

    def search_using_img(self,index,user):
        with open(f'images/c{index}.jpg', 'rb') as img:
            search_response = requests.post(self.find_url,files={'image': img}, cookies={'jwt': user.jwt_token})
        return search_response

    def get_search_result(self,query_id ):
        result_response = requests.get(self.result_url,params={"id" : query_id})
        return result_response


def main():

    user4 = User()
    t1.register_user(user4)
    t1.login_user(user4)
    find_res = t1.search_using_img(4, user4)
    find_content = json.loads(find_res.content.decode())
    time.sleep(int(find_content['time']))
    query_res = t1.get_search_result(int(find_content['id']))
    result_content = json.loads(query_res.content.decode())
    print(result_content)


def populate_database():
    user1 = User()
    user2 = User()
    user3 = User()

    mp1 = MissingPerson(1)
    mp2 = MissingPerson(2)
    mp3 = MissingPerson(3)

    t1.register_user(user1)
    t1.register_user(user2)
    t1.register_user(user3)

    t1.login_user(user1)
    t1.login_user(user2)
    t1.login_user(user3)

    t1.add_missing_person(user1, mp1)
    t1.add_missing_person(user2, mp2)
    t1.add_missing_person(user3, mp3)

    t1.logout_user(user1)
    t1.logout_user(user2)
    t1.logout_user(user3)


if __name__ == "__main__":
    t1 = TestSetUp()
    #populate_database()
    main()
