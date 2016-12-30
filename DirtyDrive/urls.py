"""DirtyDrive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from DirtyDrive import views
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^data/', views.data, name='data'),
    #url(r'^DirtyDrive/', include('DirtyDrive.urls')),
    #url(r'^$', views.index, name='index'),

    url(r'^$',  RedirectView.as_view(url='dirtyorigin', permanent=False), name='index'),
    url(r'^dirtyorigin/', views.dirtyorigin, name='dirtyorigin'),
    url(r'^dirtyzero/', views.dirtyzero, name='dirtyzero'),
    url(r'^dirtydrives/', views.dirtydrives, name='dirtydrives'),
    url(r'^about/', views.about, name='about'),
]
