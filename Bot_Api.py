import requests
import json
import random
from faker import Faker
import logging
import configparser

class Api(object):

    base_url = 'http://127.0.0.1:8000/api/'
    token_headers = {'content-type': 'application/json', 'Authorization': 'Bearer '}
    headers = {'content-type': 'application/json'}
    token = ''
    user = ''
    password = ''

    def auth(self, password, user):
        self.user = user
        self.password = password
        data = {}
        data['email'] = self.user
        data['password'] = self.password
        url = self.base_url + 'obtain_token/'
        payload = data
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        #print(r.content.decode('utf-8'))
        if r.content.decode('utf-8').find('token'):
            #print(json.loads(r.text))
            token = json.loads(r.text)["token"]
            return token
        else:
            print('Auth failed, response code: ', r.status_code)
            return r

    def create_user(self, user):
        url = self.base_url + 'user/'
        payload = user
        print('url', url, 'data', user)
        return requests.post(url, data=json.dumps(payload), headers=self.headers)

    def create_post(self, token, data):
        # self.method= 'Post'
        #data = {'title':'',
        #        'content':''}
        # #data['content'] = user[1]
        url = self.base_url + 'post/'
        payload = data
        self.token_headers['Authorization'] = 'Bearer ' + token
        r = requests.post(url, data=json.dumps(payload), headers=self.token_headers)
        return r

    def like(self, token, title):
        url = self.base_url + 'post/' + title+'/like/'
        self.token_headers['Authorization'] = 'Bearer ' + token
        r = requests.put(url, headers=self.token_headers)
        print('Response status:', r.status_code)

    def unlike(self, token, data):
        url = self.base_url + 'post/' + data['title']+'unlike/'
        self.token_headers['Authorization'] = 'Bearer ' + token
        r = requests.put(url, headers=self.token_headers)
        print('Response status:', r.status_code)


class Bot(Api):

    def __init__(self):
        self.fake = Faker()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.user_count = int(config['DEFAULT']['user_number'])
        self.max_post_per_user = int(config['DEFAULT']['max_post_per_user'])
        self.max_like_per_user = int(config['DEFAULT']['max_like_per_user'])
        logging.basicConfig(filename="Bot.log", level=logging.INFO)


    """
    Handle or random create users
    optional parameter:
    users - for custom set users
            example {"user@email.set":{"password":"12", "first_name":"Dog","last_name":"Catovich"}}
    :return users dict {"user@email.set":"password", .......}  witch status code = 202 Create
    """
    def random_or_custom_create_users(self, users=None):
        user_auth_data={}
        if users is not None:
            for user in users:
                response = self.create_user(user)
                if response.status_code == '201':
                    user_auth_data[user] = users[user]['password']
                    logging.info('Create user'+user+json.dumps(users[user]))
            if len(user_auth_data) == 0:
                raise Exception("Not response")
            return user_auth_data
        print(self.fake.ascii_free_email())
        print(self.user_count)
        for i in range(self.user_count):
            username = self.fake.ascii_free_email()
            information = {"email": username,
                           "password": self.fake.password(4),
                           "first_name": self.fake.first_name(),
                           "last_name": self.fake.last_name()}

            response = self.create_user(information)
            if response.status_code == 201:
                print('username',type(username),' ',username)
                user_auth_data[username] = information['password']
                logging.info('Create user' + username + json.dumps(information))
        if len(user_auth_data) == 0:
            raise ResponseException("not response")
        return user_auth_data

    def obtain_tokens(self, data):
        token_list = []
        for user in data:
            response = self.auth(user=user,password=data[user])
            if isinstance(response,str):
                token_list.append(response)
            else:
                logging.info(user+' token not Accepted')

        return token_list

    def create_random_post(self, tokens):
        exist_post = {}

        for token in tokens:
            for z in range(0, random.randint(0, self.max_post_per_user)):
                print(z)
                data = {'title': self.fake.text(10).replace(' ', '_').replace('.',''), 'content': self.fake.text()}
                if exist_post.get(data['title']) is None:
                    response = self.create_post(token=token, data=data)
                    if response.status_code == 201:
                        exist_post[data['title']] = token
        return exist_post

    def like_some_post(self,posts):
        title = list(posts.keys())
        users = list(posts.values())
        users_score = {}
        for i in users:
            users_score[i] = 0
        like_limit = len(users)*self.max_like_per_user
        like_count = random.randint(0,like_limit)
        for like in range(0,like_count):
            post = random.choice(title)
            user = random.choice(users)
            self.like(token=user, title=post)
            users_score[user] += 1
            if users_score[user] == self.max_like_per_user:
                users.remove(user)

def generate_info(self, users):
    bot = Bot()
    users = bot.random_or_custom_create_users()  # return email:password
    tokens = bot.obtain_tokens(users)  # return tokens
    post = bot.create_random_post(tokens)  # return title: owner_token
    bot.like_some_post(post)


class ResponseException(Exception):
    def __init__(self,m):
        self.message = m

    def __str__(self):
        return self.message
