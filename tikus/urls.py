# tikus/urls.py
from django.urls import path
from .views import AlertAPI

urlpatterns = [
    path("alert/", AlertAPI.as_view()),
]
