"""
URL configuration for gudang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from pengendali.views import SensorAPI, KipasAPI
from tikus.views import AlertAPI
from umur_simpan.views import PrediksiAPI
from core.views import beranda
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', beranda, name='beranda'),
    path('pengendali/', include('pengendali.urls')),
    path('tikus/', include('tikus.urls')),
    path('umur_simpan/', include('umur_simpan.urls')),
]
