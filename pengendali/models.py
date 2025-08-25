from django.db import models

# Create your models here.
class SensorLingkungan(models.Model):
    suhu = models.FloatField()
    kelembapan = models.FloatField()
    waktu = models.DateTimeField(auto_now_add=True)

class AktuatorKipas(models.Model):
    status = models.BooleanField(default=False)  # True = ON, False = OFF
    waktu = models.DateTimeField(auto_now_add=True)

class KonfigurasiPengendali(models.Model):
    # Mode manual
    mode_manual = models.BooleanField(default=False)
    kipas_manual = models.BooleanField(default=False)

    # Mode otomatis
    mode_otomatis = models.BooleanField(default=False)
    suhu_min = models.FloatField(default=25.0)
    suhu_max = models.FloatField(default=30.0)
    kelembapan_min = models.FloatField(default=50.0)
    kelembapan_max = models.FloatField(default=70.0)

    diperbarui = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Konfigurasi (manual={self.mode_manual}, otomatis={self.mode_otomatis})"

