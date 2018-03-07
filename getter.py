import vk


class Getter:
    VK_TIMEOUT = 10
    VK_API_VERSION = '5.35'
    VK_LANG = 'ru'

    def __init__(self, config):
        self.config = config
        session = vk.Session(access_token=config.access_token)
        self.api = vk.API(session, v=Getter.VK_API_VERSION, lang=Getter.VK_LANG, timeout=Getter.VK_TIMEOUT)

    def get(self, offset=0, count=50):
        wall_posts = self.api.wall.get(owner_id=self.config.wall_id, offset=offset, count=count)

        return Getter.format_posts(wall_posts)

    @staticmethod
    def format_posts(wall_posts):
        posts = []

        for post in reversed(wall_posts['items']):

            if not Getter.need_post(post):
                continue

            posts.append({
                'date': post['date'],
                'text': post['text'],
                'photo': Getter.photo_url_max_size(post)
            })

        return posts

    @staticmethod
    def need_post(post):
        have_attachments = ('attachments' in post) and \
                           len(post['attachments']) > 0

        have_photo = have_attachments and any(attachment['type'] == 'photo' for attachment in post['attachments'])
        have_link = have_attachments and any(attachment['type'] == 'link' for attachment in post['attachments'])
        is_ads = post['marked_as_ads'] == 1
        is_repost = 'copy_history' in post

        return have_photo and (not is_ads) and (not have_link) and (not is_repost)

    @staticmethod
    def photo_url_max_size(post):
        photo = next(attachment for attachment in post['attachments'] if attachment['type'] == 'photo')['photo']
        size = max([(int(key[6:]) if key.startswith('photo_') else 0) for key in photo.keys()])
        return photo['photo_' + str(size)]
