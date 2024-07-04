from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Configura la conexión a la base de datos
conn = psycopg2.connect(
    dbname="nombre_de_tu_base_de_datos",
    user="tu_usuario",
    password="tu_contraseña",
    host="localhost"
)
conn.autocommit = True  # Habilita el modo de autocommit para las transacciones

# Ruta para actualizar un registro en la tabla especificada
@app.route('/update/<table_name>/<int:id>', methods=['PUT'])
def update(table_name, id):
    try:
        # Crea un cursor para ejecutar consultas
        cursor = conn.cursor()

        # Construye la consulta SQL para seleccionar el registro por su ID
        cursor.execute(f"SELECT * FROM {table_name} WHERE {table_name}id=%s", (id,))
        
        # Obtén el resultado de la consulta
        record = cursor.fetchone()

        if record is None:
            return jsonify({'message': 'No se encontró el registro'}), 404

        # Aquí podrías manejar la lógica para actualizar el registro
        # Por ejemplo, puedes obtener datos de request.json y ejecutar UPDATE

        # Cierra el cursor y confirma los cambios en la base de datos
        cursor.close()
        
        return jsonify({'message': 'Registro actualizado correctamente'}), 200
    
    except Error as e:
        # Manejo de errores de psycopg2
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Asegúrate de cerrar la conexión al finalizar la operación
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)