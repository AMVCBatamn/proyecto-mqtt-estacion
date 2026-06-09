from flask import Flask, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():

    pagina = request.args.get("page", 1, type=int)

    limite = request.args.get("limit", 20, type=int)

    if limite not in [20, 50, 100]:
        limite = 20

    offset = (pagina - 1) * limite

    db = mysql.connector.connect(
        host="localhost",
        user="antonio",
        password="1234",
        database="estacion_meteorologica"
    )

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM mediciones")
    total_registros = cursor.fetchone()[0]

    total_paginas = max(1, (total_registros + limite - 1) // limite)

    cursor.execute(f"""
        SELECT
            m.id,
            e.nombre,
            s.nombre,
            CONCAT(m.valor,' ',s.unidad),
            m.fecha_hora
        FROM mediciones m
        JOIN estaciones e
            ON m.estacion_id = e.id
        JOIN sensores s
            ON m.sensor_id = s.id
        ORDER BY m.id DESC
        LIMIT {limite}
        OFFSET {offset}
    """)

    datos = cursor.fetchall()

    html = f"""
<!DOCTYPE html>

<html>

<head>

    <title>Proyecto Integrador - Grupo 6</title>

    <meta http-equiv="refresh" content="5">

    <style>

        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f9;
            margin: 30px;
        }}

        .card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }}

        h1 {{
            color: #003366;
            margin-bottom: 5px;
        }}

        h2 {{
            color: #005599;
            margin-top: 0;
        }}

        .alert {{
            background: #d4edda;
            color: #155724;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            font-weight: bold;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}

        .stat {{
            flex: 1;
            background: #003366;
            color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}

        .stat h3 {{
            margin: 0;
            font-size: 16px;
        }}

        .stat p {{
            margin: 10px 0 0;
            font-size: 28px;
            font-weight: bold;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th {{
            background: #003366;
            color: white;
            padding: 12px;
        }}

        td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}

        tr:nth-child(even) {{
            background: #f8f8f8;
        }}

        .latest {{
            background: #d4edda !important;
            font-weight: bold;
        }}

        .btn {{
            background: #003366;
            color: white;
            text-decoration: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: bold;
            margin: 5px;
            display: inline-block;
        }}

        .btn:hover {{
            background: #005599;
        }}

        .center {{
            text-align: center;
        }}

        .selector {{
            margin-top: 10px;
            margin-bottom: 15px;
        }}

    </style>

</head>

<body>

    <div class="card">

        <h1>Proyecto Integrador - Grupo 6</h1>

        <h2>Estación Meteorológica MQTT</h2>

        <div class="alert">
            Los datos se muestran en orden descendente.
            Las lecturas más recientes aparecen primero.
        </div>

        <div class="stats">

            <div class="stat">
                <h3>Total de Registros</h3>
                <p>{total_registros:,}</p>
            </div>

            <div class="stat">
                <h3>Estaciones</h3>
                <p>3</p>
            </div>

            <div class="stat">
                <h3>Sensores</h3>
                <p>5</p>
            </div>

        </div>

    </div>

    <div class="card">

        <h3>Últimas mediciones registradas</h3>

        <div class="selector">

            <b>Mostrar registros por página:</b>

            <a class="btn" href="/?page=1&limit=20">20</a>

            <a class="btn" href="/?page=1&limit=50">50</a>

            <a class="btn" href="/?page=1&limit=100">100</a>

        </div>

        <p>
            Mostrando {limite} registros por página
        </p>

        <table>

            <tr>
                <th>ID</th>
                <th>Estación</th>
                <th>Sensor</th>
                <th>Valor</th>
                <th>Fecha</th>
            </tr>
"""

    for i, fila in enumerate(datos):

        clase = "latest" if i == 0 else ""

        html += f"""
            <tr class="{clase}">
                <td>{fila[0]}</td>
                <td>{fila[1]}</td>
                <td>{fila[2]}</td>
                <td>{fila[3]}</td>
                <td>{fila[4]}</td>
            </tr>
        """

    html += f"""
        </table>

        <br>

        <div class="center">

            <a class="btn"
               href="/?page={max(1,pagina-1)}&limit={limite}">
               ← Anterior
            </a>

            <span style="
                font-size:22px;
                font-weight:bold;
                margin-left:15px;
                margin-right:15px;
            ">
                Página {pagina} de {total_paginas}
            </span>

            <a class="btn"
               href="/?page={min(total_paginas,pagina+1)}&limit={limite}">
               Siguiente →
            </a>

        </div>

        <br>

        <div class="center">

            <small style="color:gray;">
                Actualización automática cada 5 segundos
            </small>

        </div>

    </div>

</body>

</html>
"""

    cursor.close()
    db.close()

    return html


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )