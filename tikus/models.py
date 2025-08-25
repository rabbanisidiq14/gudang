from django.db import models

# Create your models here.
class AlertTikus(models.Model):
    pesan = models.CharField(max_length=200)
    waktu = models.DateTimeField(auto_now_add=True)
