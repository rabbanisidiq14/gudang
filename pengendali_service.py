import os
import django
import time
import paho.mqtt.publish as publish

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gudang.settings")
django.setup()

from pengendali.models import KonfigurasiPengendali, SensorLingkungan, AktuatorKipas

MQTT_BROKER = "localhost"
MQTT_TOPIC_KIPAS = "gudang/kipas"

# Ambil status terakhir dari DB kalau ada
try:
    last_status = AktuatorKipas.objects.latest("waktu").status
except AktuatorKipas.DoesNotExist:
    last_status = None


def loop_pengendali():
    global last_status
    while True:
        try:
            konfigurasi = KonfigurasiPengendali.objects.first()
            sensor = SensorLingkungan.objects.order_by("-waktu").first()

            if not konfigurasi or not sensor:
                time.sleep(5)
                continue

            kipas_status = False

            # Mode manual lebih prioritas
            if konfigurasi.mode_manual:
                kipas_status = konfigurasi.kipas_manual
            elif konfigurasi.mode_otomatis:
                suhu = sensor.suhu
                kelembapan = sensor.kelembapan

                if suhu > konfigurasi.suhu_max or kelembapan > konfigurasi.kelembapan_max:
                    kipas_status = True
                elif suhu < konfigurasi.suhu_min and kelembapan < konfigurasi.kelembapan_min:
                    kipas_status = False
                # kalau masih di tengah → status tetap (tidak berubah)

            # Hanya kalau status berubah, baru simpan dan publish
            if kipas_status != last_status:
                AktuatorKipas.objects.create(status=kipas_status)
                publish.single(
                    MQTT_TOPIC_KIPAS,
                    payload="ON" if kipas_status else "OFF",
                    hostname=MQTT_BROKER,
                )
                print(f"[Pengendali] Kipas {'ON' if kipas_status else 'OFF'}")
                last_status = kipas_status

        except Exception as e:
            print("Error:", e)

        time.sleep(5)


if __name__ == "__main__":
    loop_pengendali()
