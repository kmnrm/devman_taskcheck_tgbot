# Devman Tasks Check Telegram Bot
 This bot notifies [devman](https://www.facebook.com/devmanorg) students about their tasks completion. Devman students complete tasks in different [Python programming modules](https://dvmn.org/modules/). 
 
 
### Getting started

Get your **Telegram chat ID** via [userinfobot](https://telegram.me/userinfobot).

Create your Telegram Bot via [BotFather](https://telegram.me/BotFather) and get a **bot token** to access the HTTP API.

Get your **Devman Authorization token** on [devman API website](https://dvmn.org/api/docs/).


In `main.py` directory create a **`.env`** file that contains chat ID, Telegram bot token and Devman token:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
DEVMAN_TOKEN=your_devman_authorization_token
```

### How to use
Running `main.py` script:
```
$ python3 main.py
```
After a task in a module is checked, Devman Tasks Check Telegram Bot will notify a student about its completion. Each notification consists of the notification message and a task link. This bot also informs if there are any remarks made by a supervisor.

```
Проверена работа "Создайте инструмент для конкурсов в Instagram":
https://dvmn.org/modules/python-for-smm/lesson/insta-advertising/

В работе есть некоторые замечания.
```
