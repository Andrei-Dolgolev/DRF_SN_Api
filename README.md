# Test Task.
#### Create Social Network Rest Api with models User and Post.
##### Some information about project and bot using.

## Geting Started
### -Model
We create 3 model:

| User          |     | Post            |
|:-------------:| :-: |:---------------:|
| id (PK)       | :-: | id (PK)         |
| email         | :-: | owner (FK)      |
| first_name    | :-: | title           |
| last_name     | :-: | content_preview |
| city          | :-: | content         |
| ......        | :-: | ......          |

Table Like giving us infomation about how much user liked this post(multlike accepted).  


| Like          |
|:-------------:|
| owner_id (FK) |
| post_id (FK)  |
| count         |
### -URL
After we create 3 Django app user/post/like and describe his model next task it constract his routing.
So Django rest framework simple router give use next paths and metods

| URL           | Method          | Action          |
|:-------------:|:---------------:|:---------------:|
| user/         | GET             | list            |
| user/         | POST            | create          |
| user/slug     | GET             | retrieve        |
| user/slug     | PUT             | update          |
| user/slug     | PATCH           | partial_update  |
| user/slug     | DELETE          | destroy         |

This work well for User and Post model. For some actiont need need authorized user. 

##### Like

* Model using 2 view with PUT method. 

* Like
  create instance if his not exist and 
  add 1 to cont if instance exist.
  URL api/post/"title"/like 
  
* Unlike
  make count-1 and 
  desroy instance if count=0
  
#### -Authorize (JWT)
Send POST to api/user/obtain_token with walid email and password and you get token for your client side.
```
request
{email:   ,
 password:   }
```

```
response
{email:   ,
 token:   }
```
 
### -View
For Post/list add pagination and some field in serializer 

For user/create add api_call method for verify email(emailhunter.co) and get user location(clearbit.com/enrichment)

## Bot for api(Bot_Api.py)

Class Api provide as 5 methods:

* auth        # return token
* create_post
* create_user
* like
* unlike

wich makes correct request.

Class Bot read config.ini:
```
[DEFAULT]
user_number = 3
max_post_per_user = 3
max_like_per_user = 3
```
and have methods and use Api class for requests
```python
def random_or_custom_create_users(self, users=None):
    return {user:password,...} 
def obtain_tokens(self, data):
    return [token,]
def create_random_post(self, tokens):
    return {user_token:created_title,....}
def like_some_post(self,posts):
    return responce
```
#### example
```python
from Bot_Api import Bot


def generate_info(self):
    bot = Bot()
    users = bot.random_or_custom_create_users()  # return email:password
    tokens = bot.obtain_tokens(users)  # return tokens
    post = bot.create_random_post(tokens)  # return title: owner_token
    bot.like_some_post(post)
```








