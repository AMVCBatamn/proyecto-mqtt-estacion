import paho.mqtt.client as mqtt
import random
import time
import json
from datetime import datetime

BROKER = "test.mosquitto.org"
PORT = 1883

#USERNAME = "itt363-grupo6"
#PASSWORD = "jCE2XTj4Ak6g"

client = mqtt.Client()

#client.username_pw_set(USERNAME, PASSWORD)

client.connect(BROKER, PORT, 60)

print("=" * 60)
print("CONECTADO AL BROKER MQTT")
print("=" * 60)

while True:

    for estacion in range(1, 4):

        sensores = {

            "temperatura": round(random.uniform(20, 35), 2),
            "humedad": round(random.uniform(40, 95), 2),
            "viento": round(random.uniform(0, 80), 2),
            "lluvia": round(random.uniform(0, 20), 2),
            "presion": round(random.uniform(950, 1050), 2)

        }

        for sensor, valor in sensores.items():

            topic = f"/itt363-grupo6/estacion-{estacion}/sensores/{sensor}"

            payload = {

                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "estacion": estacion,
                "sensor": sensor,
                "valor": valor

            }

            client.publish(topic, json.dumps(payload))

            print("\n" + "=" * 60)
            print(f"TOPIC: {topic}")
            print("=" * 60)

            print(json.dumps(payload, indent=4))

        time.sleep(0.2)

    print("\n" + "-" * 60)
    print("Esperando nuevos datos...\n")

    time.sleep(5)