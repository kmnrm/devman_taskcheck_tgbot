import os
from time import time
import requests
from dotenv import load_dotenv
import telegram

def send_bot_message(server_response, bot, chat_id):
    host = 'https://dvmn.org'
    lesson = server_response['new_attempts'][0]['lesson_title']
    is_negative = server_response['new_attempts'][0]['is_negative']
    lesson_url = server_response['new_attempts'][0]['lesson_url']
    lesson_url = host + lesson_url
    if is_negative:
        remarks_message = 'В работе есть некоторые замечания.'
    else:
        remarks_message = 'Замечаний нет. Можно приступать к следующему уроку.'
    check_message = 'Проверена работа "{}":\n{}\n\n{}'.format(lesson, lesson_url, remarks_message)
    bot.send_message(chat_id=chat_id, text=check_message)


def get_server_response(devman_token, timestamp_param):
    headers = {
        'Authorization': 'Token %s' % devman_token
        }
    params = {'timestamp': timestamp_param}
    url = 'https://dvmn.org/api/long_polling/'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    return response


def main():
    tg_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    tg_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    devman_token = os.getenv('DEVMAN_TOKEN')
    bot = telegram.Bot(token=tg_bot_token)
    timestamp = time()
    while True:
        try:
            response = get_server_response(devman_token, timestamp)
            status = response['status']
            if status == 'timeout':
                timestamp = response['timestamp_to_request']
            else:
                timestamp = response['last_attempt_timestamp']
                send_bot_message(response, bot, tg_chat_id)
                continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue


if __name__ == "__main__":
    load_dotenv()
    main()
