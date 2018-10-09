import json
import os
import re

from django.conf import settings
from django.forms import forms


import fileupload.default_settings as DEFAULTS
from fileupload.utils import format_file_extensions


class MultiUploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self,*args,**kwargs):
        multiuploader_settings = getattr(settings, "MULTIUPLOADER_FORMS_SETTINGS", DEFAULTS.MULTIUPLOADER_FORMS_SETTINGS)
        form_type = kwargs.pop("form_type","default")

        options = {
            'maxFileSize':multiuploader_settings[form_type]["MAX_FILE_SIZE"],
            'acceptFileTypes': format_file_extensions(multiuploader_settings[form_type]["FILE_TYPES"]),
            'maxNumberOfFiles': multiuploader_settings[form_type]["MAX_FILE_NUMBER"],
            'allowedContentTypes': map(str.lower, multiuploader_settings[form_type]["CONTENT_TYPES"]),
            'autoUpload': multiuploader_settings[form_type]["AUTO_UPLOAD"]
        }

        self._options = options
        self.options = json.dumps(options)

        super().__init__(*args, **kwargs)

        self.fields["file"].widget = forms.FileInput(attrs = {'multiple':True})

    def clean_file(self):
        content = self.cleaned_data[u'file']

        filename_extension = os.path.splitext(content.name)

        if re.match(self._options['acceptFileTypes'], filename_extension, flags=re.I) is None:
            raise forms.ValidationError('acceptFileTypes')

        content_type = magic.from_buffer(content.read(1024), mime=True)

        if content_type.lower() in self._options['allowedContentTypes']:
            if content._size > self._options['maxFileSize']:
                raise forms.ValidationError("maxFileSize")
        else:
            raise forms.ValidationError("acceptFileTypes")

        return content