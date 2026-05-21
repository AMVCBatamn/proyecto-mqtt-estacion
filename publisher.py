import paho.mqtt.client as mqtt
import random
import time
import json

BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883

USERNAME = "itt363-grupo6"
PASSWORD = "jCE2XTj4Ak6g"

client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.connect(BROKER, PORT, 60)

print("Conectado al broker MQTT")

while True:

    # Simular 3 estaciones
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

                "estacion": estacion,
                "sensor": sensor,
                "valor": valor
            }

            client.publish(topic, json.dumps(payload))

            print(f"Publicado -> {topic}")
            print(payload)

    print("-" * 50)

    time.sleep(5)