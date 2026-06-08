import paho.mqtt.client as mqtt
import mysql.connector
import json
from datetime import datetime

# =========================================
# CONEXION A MARIADB
# =========================================

db = mysql.connector.connect(
    host="192.168.34.196",
    user="antonio",
    password="1234",
    database="estacion_meteorologica"
)

cursor = db.cursor()

# =========================================
# MQTT CONFIG
# =========================================

BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883

USERNAME = "itt363-grupo6"
PASSWORD = "jCE2XTj4Ak6g"

TOPIC = "/itt363-grupo6/#"

# =========================================
# MAPEO DE SENSORES
# =========================================

sensor_map = {
    "temperatura": 1,
    "humedad": 2,
    "viento": 3,
    "lluvia": 4,
    "presion": 5
}

# =========================================

def on_connect(client, userdata, flags, rc):

    print("=" * 60)
    print("CONECTADO AL BROKER MQTT")
    print("=" * 60)

    client.subscribe(TOPIC)

    print(f"Suscrito a: {TOPIC}")

# =========================================

def on_message(client, userdata, msg):

    try:

        payload = msg.payload.decode()

        data = json.loads(payload)

        estacion_id = data["estacion"]
        sensor_nombre = data["sensor"]
        valor = data["valor"]

        # Tiempo generado por el publisher
        fecha_sensor = data["timestamp"]

        # Tiempo recibido por el subscriber
        fecha_recibido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sensor_id = sensor_map[sensor_nombre]

        print("\n" + "=" * 60)
        print("NUEVO MENSAJE RECIBIDO")
        print("=" * 60)

        print(f"TOPIC            : {msg.topic}")
        print(f"ESTACION ID      : {estacion_id}")
        print(f"SENSOR           : {sensor_nombre}")
        print(f"SENSOR ID        : {sensor_id}")
        print(f"VALOR            : {valor}")
        print(f"FECHA SENSOR     : {fecha_sensor}")
        print(f"FECHA RECIBIDO   : {fecha_recibido}")

        sql = """
        INSERT INTO mediciones
        (
            estacion_id,
            sensor_id,
            valor,
            fecha_sensor,
            fecha_recibido
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            estacion_id,
            sensor_id,
            valor,
            fecha_sensor,
            fecha_recibido
        )

        cursor.execute(sql, valores)

        db.commit()

        print("\n>>> DATOS GUARDADOS EN MARIADB <<<")

    except Exception as e:

        print(f"\nERROR: {e}")

# =========================================

client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()