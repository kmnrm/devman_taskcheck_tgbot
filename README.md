# Devman Tasks Check Telegram Bot
 This bot notifies [devman](https://www.facebook.com/devmanorg) students about their tasks completion. Devman students complete tasks in different [Python programming modules](https://dvmn.org/modules/). 
 
 
## Getting started


### Get config vars

Get your **Telegram chat ID** via [userinfobot](https://telegram.me/userinfobot).

Create your Telegram Bot via [BotFather](https://telegram.me/BotFather) and get a **bot token** to access the HTTP API.

Create Logging Bot via [BotFather](https://telegram.me/BotFather) and get a **logging bot token**.

Get a **logging chat ID**, if you want to use logging bot for another Telegram account.

Get your **Devman Authorization token** on [devman API website](https://dvmn.org/api/docs/).

As a result of the steps above you will have 5 config vars:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_BOT_CHAT_ID=your_chat_id
LOGGING_BOT_TOKEN=your_logging_bot_token
LOGGING_BOT_CHAT_ID=your_logging_bot_chat_id
DEVMAN_TOKEN=your_devman_authorization_token

```
Set `LOGGING_BOT_CHAT_ID` equal to the same chat ID as your `TELEGRAM_BOT_CHAT_ID`, if you want to use both taskcheck bot and logging bot for one Telegram account. 

### Set your Heroku app

These are the instructions for activating your bot via Heroku app. If you want to run the script without creating an app on Heriku, scroll to the [Running the script](#using-this-bot) section.

1. Clone this repository to your [GitHub](https://github.com/) repositories.

2. Sign in or sign up on [Heroku](https://id.heroku.com/login), if you don't have a user account.

3. [Create new app](https://dashboard.heroku.com/new-app). Add your app name and choose a region.

4. Go to `Deploy` tab and choose `Connect to GitHub` as a deployment method to connect your Heroku app to GitHub to enable code diffs and deploys.

   Add your cloned repository name to `repo-name`, click `Search` and then click `Connect`.

   Click `Deploy Branch` to deploy `master` branch to your app. 

5. After your app successfully deployed go to `Settings` tab and add your `Config Vars`. 

   For **TELEGRAM_BOT_CHAT_ID=your_chat_id** there is `KEY` that is `TELEGRAM_BOT_CHAT_ID`, and `VALUE` that is `your_chat_id`.

   KEY  | VALUE
   ------------- | -------------
   TELEGRAM_BOT_CHAT_ID  | your_telegram_bot_token
   TELEGRAM_BOT_TOKEN  | your_chat_id
   LOGGING_BOT_CHAT_ID  | your_logging_bot_token
   LOGGING_BOT_TOKEN  | your_logging_bot_chat_id
   DEVMAN_TOKEN  | your_devman_authorization_token


### Activate your bot

Go to `Resources` to open your app [Dynos](https://www.heroku.com/dynos). You will see the line from `Procfile` in your cloned repository:
   ```
   bot python3 main.py
   ```
   Activate your bot by switching it on and clicking `Confirm`.


### Using this bot

After a task in a Devman module is checked, Devman Tasks Check Telegram Bot will notify a student about its completion. Each notification consists of the notification message and a task link. This bot also informs if there are any remarks made by a supervisor.

```
devman_task_check_bot, [01.01.20 15:37]
Проверена работа "Создайте инструмент для конкурсов в Instagram":
https://dvmn.org/modules/python-for-smm/lesson/insta-advertising/

В работе есть некоторые замечания.
```

#### Running the script

Running `main.py` script:
```
$ python3 main.py
```

Logging info:

```
2020-01-01 10:10:10,152 - INFO - Бот запущен
2020-01-01 11:10:27,210 - INFO - Прислано уведомление о проверке работы.
```

#### Logging bot

Logging bot sends a telegram message, when Tasks Check Bot has been started. 
```
logging_bot, [01.01.20 15:20]
Бот запущен
```

Logging bot sends a message if a user received a task check notification from task check bot:
```
logging_bot, [01.01.20 15:37]
Прислано уведомление о проверке работы.
```

Logging bot also notifies user about errors sending error message text: 
```
logging_bot, [01.01.20 15:30]
Бот упал с ошибкой:

logging_bot, [01.01.20 15:30]
HTTPSConnectionPool(host='dvm1n.org', port=443): Max retries exceeded with url: 
/api/long_polling/?timestamp=1587454966.4594896 
(Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x03C11630>: 
Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
```

After sending an error message bot is asleep for 10 to 20 seconds.
