import json
import logging

from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _


from fileupload.models import MultiuploaderFile
from fileupload.utils import get_thumbnail

log = logging


def fileUpload(request,noajax=False):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')

        if request.FILES is None:
            response_data = [{"error": _('Must have files attached!')}]
            return HttpResponse(json.dumps(response_data))

        # if not u'form_type' in request.POST:
        #     response_data = [{"error": _("Error when detecting form type, form_type is missing")}]
        #     return HttpResponse(json.dumps(response_data))

        file = request.FILES[u'file']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        log.info('Got file: "%s"' % filename)

        # writing file manually into model
        # because we don't need form of any type.

        fl = MultiuploaderFile()
        fl.filename = filename
        fl.file = file
        fl.save()

        log.info('File saving done')

        thumb_url = ""

        try:
            thumb_url = get_thumbnail(fl.file, "80x80", quality=50)
        except Exception as e:
            log.error(e)

        # generating json response array
        result = [{"id": fl.id.__str__(),
                   "name": filename,
                   "size": file_size,
                   "url": reverse('multiuploader_file_link', args=[fl.pk]),
                   "thumbnail_url": thumb_url,
                   "delete_url": reverse('multiuploader_delete', args=[fl.pk]),
                   "delete_type": "POST", }]

        response_data = json.dumps(result)

        # checking for json data type
        # big thanks to Guy Shapiro
        if noajax:
            if request.META['HTTP_REFERER']:
                redirect(request.META['HTTP_REFERER'])

        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            content_type = 'application/json'
        else:
            content_type = 'text/plain'
        return HttpResponse(response_data, content_type=content_type)
    else:  # GET
        return HttpResponse('Only POST accepted')


def home(request):
    return render(request,'home.html')


def multi_show_uploaded(request, pk):
    fl = get_object_or_404(MultiuploaderFile, id=pk)
    # return FileResponse(request,open(fl.file.path,'rb'), fl.name)
    imagepath = fl.file.path
    image_data = open(imagepath, "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")


def multiuploader_delete(request, pk):
    if request.method == 'POST':
        log.info('Called delete file. File id=' + str(pk))
        fl = get_object_or_404(MultiuploaderFile, pk=pk)
        fl.delete()
        log.info('DONE. Deleted file id=' + str(pk))

        return HttpResponse(1)

    else:
        log.info('Received not POST request to delete file view')
        return HttpResponseBadRequest('Only POST accepted')