# Proyecto MQTT - Estación Meteorológica

## Descripción

Este proyecto implementa una simulación de estaciones meteorológicas utilizando MQTT y el broker público de la Escuela:

mqtt.eict.ce.pucmm.edu.do

La solución permite:

- Simular múltiples estaciones meteorológicas
- Publicar datos de sensores vía MQTT
- Leer datos desde un subscriber
- Mostrar información en tiempo real por consola

## Sensores Simulados

- Temperatura
- Humedad
- Velocidad del viento
- Lluvia
- Presión atmosférica

## Jerarquía de Topics

```txt
/itt363-grupo6/estacion-1/sensores/temperatura
```

## Tecnologías Utilizadas

- Python 3
- MQTT
- paho-mqtt

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar Subscriber

```bash
python3 subscriber.py
```

## Ejecutar Publisher

```bash
python3 publisher.py
```

## Autor

Antonio Veras/Jose Espinal