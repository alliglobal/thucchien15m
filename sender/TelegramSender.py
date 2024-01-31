import logging

from concurrent.futures import ThreadPoolExecutor
#edited
from telegram import Bot
#add more
from telegram.constants import ParseMode
from telegram.error import RetryAfter
#from telegram.utils.request import Request => cai nay version cu roi
from telegram.request import HTTPXRequest

from time import sleep

import requests


class TelegramSender:

    # apiToken = '6552511028:AAFOWc_1Z5NqvdmDtPjCZJ9hp_r-R2aOXSw'
    # chatID = '-1001720823065'

    # apiToken = '5894885604:AAH5XD-0rQoi5zw23CaugRBJ45-EpbkCY88'
    # chatID = '-1002068543523'

    #THẾ GIỚI BIT CHANNEL
    apiToken = '5894885604:AAH5XD-0rQoi5zw23CaugRBJ45-EpbkCY88'
    chatID = '-1001697199458'
    
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    def __init__(
        self,
        token,
        chat_id,
        alert_chat_id=0,
        bot_emoji="\U0001F916",  # 🤖
        top_emoji="\U0001F3C6",  # 🏆
        news_emoji="\U0001F4F0",  # 📰
    ):

    


      

        # self.token = token
        #self.token = '6552511028:AAFOWc_1Z5NqvdmDtPjCZJ9hp_r-R2aOXSw'
        self.token = '5894885604:AAH5XD-0rQoi5zw23CaugRBJ45-EpbkCY88'
        # self.chat_id = chat_id
        #self.chat_id = '-1001720823065'
        #self.chat_id = '-1002068543523'
        self.chat_id = '1001697199458'
        self.alert_chat_id = alert_chat_id

        self.bot_emoji = bot_emoji
        self.top_emoji = top_emoji
        self.news_emoji = news_emoji

        self.telegram_executor = ThreadPoolExecutor(max_workers=3)

       # self.request = Request(con_pool_size=3)
        self.request = HTTPXRequest(connection_pool_size=3)
        self.bot = Bot(self.token, request=self.request)

        self.logger = logging.getLogger("telegram-sender")

    def is_alert_chat_enabled(self):
        return self.alert_chat_id != 0 and self.alert_chat_id != self.chat_id

    

    def send_to_telegram(message):

        # apiToken = '6552511028:AAFOWc_1Z5NqvdmDtPjCZJ9hp_r-R2aOXSw'
        # chatID = '-1001720823065'
        # apiToken = '5894885604:AAH5XD-0rQoi5zw23CaugRBJ45-EpbkCY88'
        # chatID = '-1002068543523'

        apiToken = '5894885604:AAH5XD-0rQoi5zw23CaugRBJ45-EpbkCY88'
        chatID = '-1001697199458'

        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

        try:
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            # print(response.text)
        except Exception as e:
            print(e)

   



    def send_message(self, message, is_alert_chat=False):
        # chat_id = self.chat_id if not is_alert_chat else self.alert_chat_id
        #chat_id = '-1002068543523'
        chat_id = '1001697199458'

        messsage = 'Halo'


        # apiToken = '6552511028:AAFOWc_1Z5NqvdmDtPjCZJ9hp_r-R2aOXSw'
        # chatID = '-1001720823065'
        # apiToken = '5894885604:AAH5XD-0rQoi5zw23CaugRBJ45-EpbkCY88'
        # chatID = '-1002068543523'

        apiToken = '5894885604:AAH5XD-0rQoi5zw23CaugRBJ45-EpbkCY88'
        chatID = '-1001697199458'


        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

        try:
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            # print(response.text)
        except Exception as e:
            print(e)


        # def send_to_telegram(message):



        def push_message(bot, chat_id, message):
            self.logger.info(message)

            # send_to_telegram("Hello from Python!")

            try:
                bot.send_message(
                    # chat_id=chat_id,
                    #chat_id = '-1002068543523',
                    chat_id = '-1001697199458',
                    text=message,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
            except RetryAfter as e:
                self.logger.error(
                    "Flood limit is exceeded. Sleep {} seconds.", e.retry_after
                )
                sleep(e.retry_after)
                # Resend message to the queue
                self.send_message(message, is_alert_chat)
            except Exception as e:
                self.logger.error(str(e))

        self.telegram_executor.submit(
            lambda p: push_message(*p), (self.bot, chat_id, message)
        )

    def send_generic_message(self, message, args=None, is_alert_chat=False):
        if args is not None:
            message = message.format(args)
        self.send_message(self.bot_emoji + " " + message, is_alert_chat)

    def send_report_message(self, message, args=None, is_alert_chat=False):
        if args is not None:
            message = message.format(args)
        self.send_message(self.top_emoji + " " + message, is_alert_chat)

    def send_news_message(self, message, args=None, is_alert_chat=False):
        if args is not None:
            message = message.format(args)
        self.send_message(self.news_emoji + " " + message, is_alert_chat)
