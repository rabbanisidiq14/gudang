from django import forms
from .models import PrediksiUmurSimpan, Produk
import math

class PrediksiForm(forms.ModelForm):
    class Meta:
        model = PrediksiUmurSimpan
        fields = ["produk", "kadar_air", "suhu", "kelembapan"]
        widgets = {
            "kadar_air": forms.NumberInput(attrs={"step": 0.1, "min": 0}),
            "suhu": forms.NumberInput(attrs={"step": 0.1}),
            "kelembapan": forms.NumberInput(attrs={"step": 0.1, "min": 0, "max": 100}),
        }

    def bersihkan_dan_hitung(self):
        """
        Mengembalikan tuple (umur_hari_int, aw_float) memakai rumus Harrington:
        L0=365; MC0=12.5; T0=22. Rumus: L0 * 2**(MC0 - MC) * 2**((T0 - T)/5.6)
        aw = RH/100
        """
        L0 = 365.0
        MC0 = 12.5
        T0 = 22.0

        MC = float(self.cleaned_data["kadar_air"])
        T = float(self.cleaned_data["suhu"])
        RH = float(self.cleaned_data["kelembapan"])

        umur_simpan = L0 * (2 ** (MC0 - MC)) * (2 ** ((T0 - T) / 5.6))
        aw = RH / 100.0
        return (max(0, math.floor(umur_simpan)), aw)


class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ["nama", "jenis", "keterangan"]
        widgets = {
            "keterangan": forms.Textarea(attrs={"rows": 3}),
        }
