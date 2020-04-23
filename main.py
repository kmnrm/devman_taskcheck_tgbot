import os
from time import time, sleep
import logging
import requests
from dotenv import load_dotenv
import telegram


class MyLogsHandler(logging.Handler):
    def __init__(self, logging_bot_token, chat_id):
        super().__init__()
        self.logging_bot = telegram.Bot(token=logging_bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.logging_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_bot_message(server_response, bot, chat_id):
    host = 'https://dvmn.org'
    solution_attempt = server_response['new_attempts'][0]
    lesson = solution_attempt['lesson_title']
    is_negative = solution_attempt['is_negative']
    lesson_url = solution_attempt['lesson_url']
    lesson_url = '{}{}'.format(host, lesson_url)
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


def create_logger(token, chat_id):
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = MyLogsHandler(token, chat_id)
    logger.addHandler(handler)
    return logger


def main():
    logging_bot_token = os.environ['LOGGING_BOT_TOKEN']
    logging_chat_id = os.environ['LOGGING_BOT_CHAT_ID']
    logger = create_logger(logging_bot_token, logging_chat_id)
    logger.info("Бот запущен")
    while True:
        try:
            tg_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
            tg_chat_id = os.environ['TELEGRAM_BOT_CHAT_ID']
            devman_token = os.environ['DEVMAN_TOKEN']
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
                        logger.info("Прислано уведомление о проверке работы.")
                        continue
                except requests.exceptions.ReadTimeout as readtimeout_error:
                    logger.error("Бот упал с ошибкой:")
                    logger.error(readtimeout_error)
                except requests.exceptions.ConnectionError as connection_error:
                    logger.error("Бот упал с ошибкой:")
                    logger.error(connection_error)
                    sleep(10)
        except Exception as err:
            logger.exception("Бот упал с ошибкой:")
            sleep(20)


if __name__ == "__main__":
    load_dotenv()
    main()
