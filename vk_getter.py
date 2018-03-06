import time
import vk
import telegram
import urllib.request
import ssl
import yaml
import io
from PIL import Image, ImageDraw, ImageFont

with open("data.yaml", 'r') as stream:
    data = yaml.load(stream)

session = vk.Session(access_token=data['access_token'])
api = vk.API(session, v='5.35', lang='ru', timeout=10)

wall = api.wall.get(owner_id=data['owner_id'], count=50, offset=0)

bot = telegram.Bot(token=data['telegram_token'])

last_date = data['last_date']
ssl._create_default_https_context = ssl._create_unverified_context

print(wall)
for post in reversed(wall['items']):
    if post['date'] <= last_date:
        continue
    text = post['text']
    print('-----')
    print(post['date'])
    print('------')
    if ('attachments' in post) and len(post['attachments']) > 0 and post['attachments'][0]['type'] == 'photo':
        photo = post['attachments'][0]['photo']
        size = max([(int(key[6:]) if key.startswith('photo_') else 0) for key in photo.keys()])
        photo_url = photo['photo_' + str(size)]

        """if len(text) > 200:
            bot.send_photo(chat_id='@rhymeseen', photo=photo_url, timeout=60)
            phot = bot.send_message(chat_id='@rhymeseen', text=text, timeout=60)
        else:
            phot = bot.send_photo(chat_id='@rhymeseen', photo=photo_url, caption=text, timeout=60)
        print(phot)"""

        file_name, headers = urllib.request.urlretrieve(photo_url)

        base = Image.open(file_name).convert('RGBA')

        base.thumbnail((500, 500), Image.ANTIALIAS)

        fnt = ImageFont.truetype('Roboto-Regular.ttf', 40)

        tmp_d = ImageDraw.Draw(base)

        sizes = tmp_d.multiline_textsize(text, fnt)

        width, height = base.size

        text_width, text_height = sizes
        text_width = text_width + 100

        left = 0

        if text_width > width:
            left = int((text_width - width) / 2)
            width = text_width

        height = height + text_height + 100

        txt = Image.new('RGBA', (width, height), (255, 255, 255, 255))

        d = ImageDraw.Draw(txt)

        d.multiline_text((50, 50), text, font=fnt, fill=(0, 0, 0, 255))

        txt.paste(base, (left, text_height + 100))

        # txt.show()

        txt.save('tmp.png')

        days_file = open('tmp.png', 'rb')

        phot = bot.send_photo(chat_id='@rhymeseen', photo=days_file, timeout=60)

    last_date = post['date']
    time.sleep(5)

print(last_date)

data['last_date'] = last_date

with io.open('data.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
