import os
import telegram
import time

from image_maker import ImageMaker


class Sender:
    TELEGRAM_TIMEOUT = 60

    def __init__(self, config):
        self.config = config
        self.bot = telegram.Bot(token=config.telegram_token)

    def send_posts(self, posts):
        for post in posts:
            self.send_post(post)

            time.sleep(5)

    def send_post(self, post):
        if post['date'] <= self.config.last_date:
            return
        file_descriptor, path = ImageMaker.make(post)

        picture = open(path, 'rb')

        self.bot.send_photo(chat_id=self.config.telegram_chat_id, photo=picture, timeout=Sender.TELEGRAM_TIMEOUT)

        picture.close()
        os.close(file_descriptor)

        self.config.last_date = post['date']
        self.config.save_config()
