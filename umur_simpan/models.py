from django.db import models

class Produk(models.Model):
    JENIS_CHOICES = (
        ("gabah", "Gabah"),
        ("beras", "Beras"),
    )
    nama = models.CharField(max_length=100)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default="gabah")
    keterangan = models.TextField(blank=True, null=True)
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} ({self.get_jenis_display()})"


class PrediksiUmurSimpan(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name="prediksi")
    kadar_air = models.FloatField(help_text="Dalam persen, misal 12.5")
    suhu = models.FloatField(help_text="Suhu (°C)")
    kelembapan = models.FloatField(help_text="RH (%)")
    umur_hari = models.IntegerField()
    aw = models.FloatField()
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediksi {self.produk} - {self.umur_hari} hari"
