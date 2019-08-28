# Quiz Bot

This quiz bot using txt-files with questions and anwsers (see **quiz-questions** directory). Actually, there are two bots  - Telegram Bot and VKontakte Bot. For storing current answers they use [Redis](https://redislabs.com/) database. You can check out them right now: TG: @quiz_chat_bot, VK: club183180897


## How to install

1. Python 3.6 and libraries from **requirements.txt** should be installed.

```bash
$ pip install -r requirements.txt
```

2. Create new Telegram bot, get token and your ID.

3. Create new VK group (or use exists), get API token of the group and allow the group to write messages.

4. Create Redis account, get host, port and password.

5. Put all necessary parameters to .env file.

```
TOKEN_TG=telegram_token
CHAT_ID_TG_ADMIN=telegram_chat_id_admin
REDIS_HOST=redis_host
REDIS_PORT=redis_port
REDIS_PWD=redis_password
TOKEN_VK=token_vkontakte

```


## Quickstart

Run **main_tg.py** and **main_vk.py** files and test the both.


## How to deploy

For example, you can deploy apps on [Heroku](https://heroku.com), with
GitHub integration.

1. Create two apps on Heroku with GitHub deployment method.

2. Add necessary environment variables to Settings > Config Vars section of every app.

3. Activate your Dyno in the "Resourses" section.

For reading logs install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and log in.

```bash
$ heroku logs -a your-app-name
```

Of course, you can create and manage your apps directly from the Heroku CLI.


## Project Goals

The code is written for educational purposes on online-course for
web-developers [dvmn.org](https://dvmn.org/).
