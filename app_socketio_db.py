from flask import Flask
from flask_socketio import SocketIO
import mysql.connector
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

ultimo_id = 0

def monitorear_bd():
    global ultimo_id

    while True:

        try:

            db = mysql.connector.connect(
                host="localhost",
                user="antonio",
                password="1234",
                database="estacion_meteorologica"
            )

            cursor = db.cursor()

            cursor.execute("""
                SELECT
                    m.id,
                    e.nombre,
                    s.nombre,
                    CONCAT(m.valor,' ',s.unidad),
                    m.fecha_hora
                FROM mediciones m
                JOIN estaciones e
                    ON m.estacion_id=e.id
                JOIN sensores s
                    ON m.sensor_id=s.id
                ORDER BY m.id DESC
                LIMIT 1
            """)

            fila = cursor.fetchone()

            if fila and fila[0] != ultimo_id:

                ultimo_id = fila[0]

                socketio.emit("nueva_medicion", {
                    "id": fila[0],
                    "estacion": fila[1],
                    "sensor": fila[2],
                    "valor": fila[3],
                    "fecha": str(fila[4])
                })

                print("EMIT:", fila[0])

            cursor.close()
            db.close()

        except Exception as e:
            print(e)

        time.sleep(1)

@app.route("/")
def home():

    return """
<!DOCTYPE html>

<html>

<head>

    <title>SocketIO MQTT Test</title>

    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

</head>

<body>

    <h1>SocketIO MQTT Test</h1>

    <div id="resultado">

        Esperando conexión...

    </div>

    <script>

        const socket = io();

        socket.on("connect", function() {

            document.getElementById("resultado").innerHTML =
                "<h2 style='color:green'>SOCKET CONECTADO</h2>";

            console.log("SOCKET CONECTADO");

        });

        socket.on("disconnect", function() {

            document.getElementById("resultado").innerHTML =
                "<h2 style='color:red'>SOCKET DESCONECTADO</h2>";

            console.log("SOCKET DESCONECTADO");

        });

        socket.on("nueva_medicion", function(data) {

            document.getElementById("resultado").innerHTML =
                `
                <h2 style="color:green">NUEVA MEDICIÓN RECIBIDA</h2>

                <p><b>ID:</b> ${data.id}</p>

                <p><b>Estación:</b> ${data.estacion}</p>

                <p><b>Sensor:</b> ${data.sensor}</p>

                <p><b>Valor:</b> ${data.valor}</p>

                <p><b>Fecha:</b> ${data.fecha}</p>
                `;

            console.log(data);

        });

    </script>

</body>

</html>
"""

if __name__ == "__main__":

    hilo = threading.Thread(
        target=monitorear_bd,
        daemon=True
    )

    hilo.start()

    socketio.run(
        app,
        host="0.0.0.0",
        port=8080
    )