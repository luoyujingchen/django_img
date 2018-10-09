from _sha1 import sha1
from random import choice
from django.conf import settings
from PIL import Image, ImageOps

def generate_safe_pk(self):
    from base64 import b32encode
    from hashlib import sha1
    from random import random
    rude = ('lol',)
    bad_pk = True
    while bad_pk:
        pk = b32encode(sha1(str(random())).digest()).lower()[:6]
        bad_pk = False
        for rw in rude:
            if pk.find(rw) >= 0: bad_pk = True
    return pk


def get_thumbnail(img, thumb_size, quality=80, format='JPG'):

    thumb_size = thumb_size.split('x')

    img.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)

    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    # get size
    thumb_w = int(thumb_size[0])
    thumb_h = int(thumb_size[1])
    image2 = ImageOps.fit(image, (thumb_w, thumb_h), Image.ANTIALIAS)

    # raise Exception( img )
    split = img.path.rsplit('.', 1)
    try:
        thumb_url = '%s.%sx%s.%s' % (split[0], thumb_w, thumb_h, split[1])
    except:
        thumb_url = '%s.%sx%s' % (split, thumb_w, thumb_h)
    # PNG and GIF are the same, JPG is JPEG
    if format.upper() == 'JPG':
        format = 'JPEG'

    image2.save(thumb_url, format, quality=quality)
    return thumb_url.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace('//', '/')


#Getting files here
def format_file_extensions(extensions):
    return  ".(%s)$" % "|".join(extensions)