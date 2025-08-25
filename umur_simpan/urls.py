# umur_simpan/urls.py
from django.urls import path
from .views import PrediksiAPI

urlpatterns = [
    path("prediksi/", PrediksiAPI.as_view()),
]
