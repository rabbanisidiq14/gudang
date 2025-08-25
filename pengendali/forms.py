from django import forms
from .models import KonfigurasiPengendali

class KonfigurasiForm(forms.ModelForm):
    class Meta:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Jika mode_manual aktif, disable field histeresis dan tidak required
            if self.instance.mode_manual:
                for f in ["suhu_min", "suhu_max", "kelembapan_min", "kelembapan_max"]:
                    self.fields[f].required = False
                    self.fields[f].widget.attrs['disabled'] = True
        model = KonfigurasiPengendali
        fields = [
            "suhu_min", "suhu_max", "kelembapan_min", "kelembapan_max"
        ]
        widgets = {
            'suhu_min': forms.NumberInput(attrs={'step': 0.1}),
            'suhu_max': forms.NumberInput(attrs={'step': 0.1}),
            'kelembapan_min': forms.NumberInput(attrs={'step': 1}),
            'kelembapan_max': forms.NumberInput(attrs={'step': 1}),
        }
        

