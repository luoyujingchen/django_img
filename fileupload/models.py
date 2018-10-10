import datetime
import os
import uuid
import hashlib
from django.conf import settings
from django.db import models
from django.utils.text import get_valid_filename
from django.utils.translation import ugettext_lazy as _

import fileupload.default_settings as DEFAULTS

# Create your models here.

class BaseAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),editable=False)
    name = models.CharField(max_length=255)
    # ac_by = models.ForeignKey(to=Dish, on_delete=models.CASCADE)
    upload_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.upload_date:
            self.upload_date = datetime.datetime.now()

        super().save(*args, **kwargs)

class MultiuploaderFile(BaseAttachment):
    def _upload_to(instance, filename):
        upload_path = getattr(settings, 'MULTIUPLOADER_FILES_FOLDER', DEFAULTS.MULTIUPLOADER_FILES_FOLDER)

        if upload_path[-1] != '/':
            upload_path += '/'

        filename = get_valid_filename(os.path.basename(filename))
        filename, ext = os.path.splitext(filename)
        hash = hashlib.sha1(str(datetime.time()).encode('utf-8')).hexdigest()
        fullname = os.path.join(upload_path, "%s.%s%s" % (filename, hash, ext))

        return fullname

    file = models.FileField(upload_to=_upload_to, max_length=255)

    def save(self, *args, **kwargs):
        self.filename = os.path.basename(self.file.path)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('multiuploader file')
        verbose_name_plural = _('multiuploader files')
