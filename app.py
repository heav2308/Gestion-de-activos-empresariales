from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL
def connect_postgres():
    conn = psycopg2.connect(
        dbname="Ejercicio Gestión de Activos Empresariales",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    return conn

# Función para obtener todas las tablas de la base de datos
def get_tables():
    conn = connect_postgres()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

# Función para obtener datos de una tabla específica
def get_table_data(table_name):
    conn = connect_postgres()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}'")
    columns = cursor.fetchall()
    conn.close()
    return data, [column[0] for column in columns]

# Ruta para mostrar la lista de tablas
@app.route('/')
def index():
    tables = get_tables()
    return render_template('index.html', tables=tables)

# Ruta para mostrar los datos de una tabla específica
@app.route('/table/<table_name>')
def table(table_name):
    data, columns = get_table_data(table_name)
    return render_template('table.html', table_name=table_name, data=data, columns=columns)

# Ruta para crear un nuevo registro
@app.route('/table/<table_name>/create', methods=['GET', 'POST'])
def create(table_name):
    if request.method == 'POST':
        conn = connect_postgres()
        cursor = conn.cursor()
        columns = ', '.join(request.form.keys())
        values = ', '.join([f"%({key})s" for key in request.form.keys()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(sql, request.form)
        conn.commit()
        conn.close()
        return redirect(url_for('table', table_name=table_name))
    _, columns = get_table_data(table_name)
    return render_template('create.html', table_name=table_name, columns=columns)

# Ruta para actualizar un registro existente
@app.route('/table/<table_name>/update/<int:id>', methods=['GET', 'POST'])
def update(table_name, id):
    conn = connect_postgres()
    cursor = conn.cursor()
    if request.method == 'POST':
        updates = ', '.join([f"{key}=%({key})s" for key in request.form.keys()])
        sql = f"UPDATE {table_name} SET {updates} WHERE id={id}"
        cursor.execute(sql, request.form)
        conn.commit()
        conn.close()
        return redirect(url_for('table', table_name=table_name))
    cursor.execute(f"SELECT * FROM {table_name} WHERE id={id}")
    record = cursor.fetchone()
    _, columns = get_table_data(table_name)
    conn.close()
    return render_template('update.html', table_name=table_name, record=record, columns=columns)

# Ruta para eliminar un registro
@app.route('/table/<table_name>/delete/<int:id>')
def delete(table_name, id):
    conn = connect_postgres()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id={id}")
    conn.commit()
    conn.close()
    return redirect(url_for('table', table_name=table_name))

if __name__ == '__main__':
    app.run(debug=True)