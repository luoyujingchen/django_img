"""fileupload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from fileupload import views

urlpatterns = [
    path('',views.home),
    path('upload',views.fileUpload),
    re_path(r'^multiuploader_file/(?P<pk>\w*)/$', views.multi_show_uploaded,
        name='multiuploader_file_link'),
    re_path(r'^multiuploader_delete/(?P<pk>\w+)/$', views.multiuploader_delete,
       name='multiuploader_delete'),
]
