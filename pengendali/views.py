from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SensorLingkungan, AktuatorKipas
import paho.mqtt.publish as publish
from .models import KonfigurasiPengendali
from .forms import KonfigurasiForm

# Create your views here.

MQTT_BROKER = "localhost"
MQTT_TOPIC_SENSOR = "gudang/sensor"
MQTT_TOPIC_KIPAS = "gudang/kipas"

def halaman_sensor(request):
    return render(request, "pengendali/halaman_sensor.html")

class SensorAPI(APIView):
    def get(self, request):
        data = SensorLingkungan.objects.order_by('-waktu')[:10]
        return Response([{"suhu": d.suhu, "kelembapan": d.kelembapan, "waktu": d.waktu} for d in data])

class KipasAPI(APIView):
    def post(self, request):
        status = request.data.get("status", False)
        AktuatorKipas.objects.create(status=status)
        publish.single(MQTT_TOPIC_KIPAS, payload="ON" if status else "OFF", hostname=MQTT_BROKER)
        return Response({"pesan": f"Kipas {'ON' if status else 'OFF'}"})

def konfigurasi_pengendali(request):
    konfigurasi, _ = KonfigurasiPengendali.objects.get_or_create(id=1)

    if request.method == "POST":
        # 1️⃣ Cek apakah JSON dari toggle
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                if "mode_manual" in data:
                    konfigurasi.mode_manual = data["mode_manual"]
                    konfigurasi.mode_otomatis = data.get("mode_otomatis", not data["mode_manual"])
                    # Simpan langsung
                    konfigurasi.save()
                    return JsonResponse({
                        "status": "ok",
                        "mode_manual": konfigurasi.mode_manual,
                        "mode_otomatis": konfigurasi.mode_otomatis
                    })
                if "kipas_manual" in data:
                    konfigurasi.kipas_manual = data["kipas_manual"]
                    konfigurasi.save()
                    return JsonResponse({
                        "status": "ok",
                        "kipas_manual": konfigurasi.kipas_manual
                    })
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        # 2️⃣ POST dari form biasa (ubah suhu/kelembapan)
        form = KonfigurasiForm(request.POST, instance=konfigurasi)

        # 🔹 Jika mode_manual, disable required untuk field histeresis
        if konfigurasi.mode_manual:
            for f in ["suhu_min", "suhu_max", "kelembapan_min", "kelembapan_max"]:
                form.fields[f].required = False

        if form.is_valid():
            form.save()
            return redirect("konfigurasi_pengendali")
    else:
        form = KonfigurasiForm(instance=konfigurasi)
        # 🔹 Jika manual, juga nonaktifkan required di form
        if konfigurasi.mode_manual:
            for f in ["suhu_min", "suhu_max", "kelembapan_min", "kelembapan_max"]:
                form.fields[f].required = False

    return render(request, "pengendali/konfigurasi.html", {"form": form})


