from Bot_Api import Bot


def generate_info():
    bot = Bot()
    users = bot.random_or_custom_create_users()  # return {email:password, ...}
    tokens = bot.obtain_tokens(users)  # return tokens [,,,,]
    post = bot.create_random_post(tokens)  # return {title: owner_title_token,...}
    bot.like_some_post(post)

if __name__ == '__main__':
    generate_info()