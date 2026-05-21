import paho.mqtt.client as mqtt

BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883

USERNAME = "itt363-grupo6"
PASSWORD = "jCE2XTj4Ak6g"

TOPIC = "/itt363-grupo6/#"

def on_connect(client, userdata, flags, rc):

    print("Conectado al broker MQTT")

    client.subscribe(TOPIC)

    print(f"Suscrito a: {TOPIC}")

def on_message(client, userdata, msg):

    print("\nMensaje recibido")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {msg.payload.decode()}")

client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()