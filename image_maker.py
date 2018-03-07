import tempfile
import urllib.request
import ssl
from PIL import Image, ImageDraw, ImageFont


class ImageMaker:
    FONT_PATH = 'Roboto-Regular.ttf'
    FONT_SIZE = 40
    FONT_COLOR = (0, 0, 0, 255)

    BACKGROUND_COLOR = (255, 255, 255, 255)

    THUMBNAIL_SIZE = (500, 500)
    
    PADDING_TOP = 50
    PADDING_BOTTOM = 50
    PADDING_LEFT = 50
    PADDING_RIGHT = 50

    @staticmethod
    def make(post):
        ssl._create_default_https_context = ssl._create_unverified_context
        tmp_file, _ = urllib.request.urlretrieve(post['photo'])

        base_image = Image.open(tmp_file).convert('RGBA')

        base_image.thumbnail(ImageMaker.THUMBNAIL_SIZE, Image.ANTIALIAS)

        font = ImageFont.truetype(ImageMaker.FONT_PATH, ImageMaker.FONT_SIZE)

        tmp_image_draw = ImageDraw.Draw(base_image)

        image_width, image_height = base_image.size
        text_width, text_height = tmp_image_draw.multiline_textsize(post['text'], font)

        text_width = text_width + ImageMaker.PADDING_LEFT + ImageMaker.PADDING_RIGHT

        image_height = image_height + text_height + ImageMaker.PADDING_TOP + ImageMaker.PADDING_BOTTOM
        image_top = text_height + ImageMaker.PADDING_TOP + ImageMaker.PADDING_BOTTOM
        
        image_left = 0

        if text_width > image_width:
            image_left = int((text_width - image_width) / 2)
            image_width = text_width

        result_image = Image.new('RGBA', (image_width, image_height), ImageMaker.BACKGROUND_COLOR)

        result_image_draw = ImageDraw.Draw(result_image)

        result_image_draw.multiline_text((ImageMaker.PADDING_LEFT, ImageMaker.PADDING_TOP), post['text'], font=font,
                                         fill=ImageMaker.FONT_COLOR)

        result_image.paste(base_image, (image_left, image_top))

        result_file_descriptor, result_path = tempfile.mkstemp('.png')

        result_image.save(result_path)

        return result_file_descriptor, result_path
