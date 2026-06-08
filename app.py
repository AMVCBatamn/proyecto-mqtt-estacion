from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():

    mediciones = [
        {
            "id": 32163,
            "estacion": "Estacion 3",
            "sensor": "presion",
            "valor": "1042.36 hPa",
            "fecha": "2026-06-08 16:18:25"
        },
        {
            "id": 32162,
            "estacion": "Estacion 3",
            "sensor": "lluvia",
            "valor": "5.78 mm",
            "fecha": "2026-06-08 16:18:25"
        },
        {
            "id": 32161,
            "estacion": "Estacion 3",
            "sensor": "viento",
            "valor": "64.63 km/h",
            "fecha": "2026-06-08 16:18:25"
        }
    ]

    return render_template(
        "index.html",
        mediciones=mediciones
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )