import os
import django
import json
import paho.mqtt.client as mqtt

# Konfigurasi Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gudang.settings")
django.setup()

from pengendali.models import SensorLingkungan

MQTT_BROKER = "192.168.55.118"
MQTT_TOPIC = "gudang/sensor"

def on_connect(client, userdata, flags, rc):
    print("Terhubung ke MQTT Broker dengan kode:", rc)
    client.subscribe(MQTT_TOPIC)

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
    
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)  # asumsi kirim JSON {"suhu": 25.3, "kelembapan": 60}
        suhu = safe_float(data.get("suhu"))
        kelembapan = safe_float(data.get("kelembapan"))


        # simpan ke database
        SensorLingkungan.objects.create(suhu=suhu, kelembapan=kelembapan)
        print(f"Data disimpan: Suhu={suhu}, Kelembapan={kelembapan}")
    except Exception as e:
        print("Error:", e)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
