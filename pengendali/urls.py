# pengendali/urls.py
from django.urls import path
from .views import SensorAPI, KipasAPI, halaman_sensor, konfigurasi_pengendali

urlpatterns = [
    path("sensor/", SensorAPI.as_view()),
    path("monitor/", halaman_sensor, name="halaman_sensor"),
    path("konfigurasi/", konfigurasi_pengendali, name="konfigurasi_pengendali"),
]
