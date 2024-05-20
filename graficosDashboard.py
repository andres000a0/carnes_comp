from flask import Flask, session
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '192.168.33.251'
app.config['MYSQL_USER'] = 'miguelos'
app.config['MYSQL_PASSWORD'] = 'Mosorio2022$'
app.config['MYSQL_DB'] = 'comp_cajeros'

mysql = MySQL(app)

def generate_chart_data():
    cur = mysql.connection.cursor()
    # Datos de ejemplo
     # Consulta la base de datos para obtener los datos de productividad por caja
    cur.execute("SELECT id_caja, COUNT(*) AS productividad FROM cajeros WHERE id_co = %s GROUP BY id_caja", (session["sede"],))
    cajas_productividad = cur.fetchall()

    # Procesa los datos para la gráfica
    cajas_nombres = []
    productividad = []

    for caja in cajas_productividad:
        cajas_nombres.append(caja[0])
        productividad.append(caja[1])

    cur.close()

    # Crear datos en el formato adecuado para Chart.js para productividad por registros
    productividad_data = {
        'labels': cajas_nombres,
        'datasets': [
            {
                'label': 'Productividad por Registros',
                'data': productividad,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1,
                'type': 'bar'
            }
        ]
    }

    # Crear datos en el formato adecuado para Chart.js para tiempo de inactividad
    inactividad_data = {
        'labels': cajas_nombres,
        'datasets': [
            {
                'label': 'Tiempo de Inactividad de las Cajas',
                'data': cajas_nombres,
                'fill': False,
                'borderColor': 'rgba(255, 99, 132, 0.8)',
                'type': 'line'
            }
        ]
    }

    # Convertir los datos a JSON
    productividad_data_json = json.dumps(productividad_data)
    inactividad_data_json = json.dumps(inactividad_data)

    return productividad_data_json, inactividad_data_json