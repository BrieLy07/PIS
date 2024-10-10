from flask import Flask, render_template, request, redirect, url_for, make_response
import pymysql
from config import get_db_connection
import pdfkit

app = Flask(__name__)

# Ruta principal
@app.route('/home')
def home():
    return render_template('home.html')

# Ruta para Equipos
# Ruta para listar equipos
@app.route('/equipos')
def equipos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT equipos.id, equipos.nombre_E, equipos.modelo, equipos.serial, 
               usuarios.nombre_U, categorias.nombre_C
        FROM equipos
        LEFT JOIN usuarios ON equipos.usuario_id = usuarios.id
        LEFT JOIN categorias ON equipos.categoria_id = categorias.id
    """)
    equipos = cursor.fetchall()
    conn.close()
    return render_template('equipos.html', equipos=equipos)

# Ruta para agregar un nuevo equipo
@app.route('/equipos/agregar', methods=['GET', 'POST'])
def agregar_equipo():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_E = request.form['nombre_E']
        modelo = request.form['modelo']
        serial = request.form['serial']
        especificaciones = request.form['especificaciones']
        usuario_id = request.form['usuario_id']
        categoria_id = request.form['categoria_id']

        cursor.execute("""
            INSERT INTO equipos (nombre_E, modelo, serial, especificaciones, usuario_id, categoria_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_E, modelo, serial, especificaciones, usuario_id, categoria_id))
        conn.commit()
        conn.close()
        return redirect(url_for('equipos'))

    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    conn.close()
    return render_template('agregar_equipo.html', usuarios=usuarios, categorias=categorias)

# Ruta para editar un equipo
@app.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_E = request.form['nombre_E']
        modelo = request.form['modelo']
        serial = request.form['serial']
        especificaciones = request.form['especificaciones']
        usuario_id = request.form['usuario_id']
        categoria_id = request.form['categoria_id']

        cursor.execute("""
            UPDATE equipos SET nombre_E = %s, modelo = %s, serial = %s, 
                               especificaciones = %s, usuario_id = %s, categoria_id = %s 
            WHERE id = %s
        """, (nombre_E, modelo, serial, especificaciones, usuario_id, categoria_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('equipos'))

    cursor.execute('SELECT * FROM equipos WHERE id = %s', (id,))
    equipo = cursor.fetchone()

    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    conn.close()

    return render_template('editar_equipo.html', equipo=equipo, usuarios=usuarios, categorias=categorias)

# Ruta para eliminar un equipo
@app.route('/equipos/eliminar/<int:id>', methods=['GET'])
def eliminar_equipo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipos WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('equipos'))

# Ruta para Usuarios
# Ruta para listar usuarios
@app.route('/usuarios')
def usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT usuarios.id, usuarios.nombre_U, usuarios.cedula_U, departamentos.nombre_D 
        FROM usuarios 
        LEFT JOIN departamentos ON usuarios.departamento_id = departamentos.id
    """)
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

# Ruta para agregar un nuevo usuario
@app.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_U = request.form['nombre_U']
        cedula_U = request.form['cedula_U']
        departamento_id = request.form['departamento_id']

        cursor.execute("""
            INSERT INTO usuarios (nombre_U, cedula_U, departamento_id) 
            VALUES (%s, %s, %s)
        """, (nombre_U, cedula_U, departamento_id))
        conn.commit()
        conn.close()
        return redirect(url_for('usuarios'))

    cursor.execute('SELECT * FROM departamentos')
    departamentos = cursor.fetchall()
    conn.close()
    return render_template('agregar_usuario.html', departamentos=departamentos)

# Ruta para editar un usuario
@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_U = request.form['nombre_U']
        cedula_U = request.form['cedula_U']
        departamento_id = request.form['departamento_id']

        cursor.execute("""
            UPDATE usuarios SET nombre_U = %s, cedula_U = %s, departamento_id = %s 
            WHERE id = %s
        """, (nombre_U, cedula_U, departamento_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('usuarios'))

    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    usuario = cursor.fetchone()

    cursor.execute('SELECT * FROM departamentos')
    departamentos = cursor.fetchall()
    conn.close()

    return render_template('editar_usuario.html', usuario=usuario, departamentos=departamentos)

# Ruta para eliminar un usuario
@app.route('/usuarios/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('usuarios'))


# Ruta para Departamentos
# Ruta para listar departamentos
@app.route('/departamentos')
def departamentos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM departamentos')
    departamentos = cursor.fetchall()
    conn.close()
    return render_template('departamentos.html', departamentos=departamentos)

# Ruta para agregar un nuevo departamento (GET para mostrar formulario, POST para procesar el formulario)
@app.route('/departamentos/agregar', methods=['GET', 'POST'])
def agregar_departamento():
    if request.method == 'POST':
        nombre_D = request.form['nombre_D']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO departamentos (nombre_D) VALUES (%s)', (nombre_D,))
        conn.commit()
        conn.close()
        return redirect(url_for('departamentos'))
    return render_template('agregar_departamento.html')

# Ruta para editar un departamento
@app.route('/departamentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_departamento(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_D = request.form['nombre_D']
        cursor.execute('UPDATE departamentos SET nombre_D = %s WHERE id = %s', (nombre_D, id))
        conn.commit()
        conn.close()
        return redirect(url_for('departamentos'))

    cursor.execute('SELECT * FROM departamentos WHERE id = %s', (id,))
    departamento = cursor.fetchone()
    conn.close()
    return render_template('editar_departamento.html', departamento=departamento)

# Ruta para eliminar un departamento
@app.route('/departamentos/eliminar/<int:id>', methods=['GET'])
def eliminar_departamento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM departamentos WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('departamentos'))

# Ruta para listar categorías
@app.route('/categorias')
def categorias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

# Ruta para agregar categoría
@app.route('/categorias/agregar', methods=['GET', 'POST'])
def agregar_categoria():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_C = request.form['nombre_C']
        cursor.execute('INSERT INTO categorias (nombre_C) VALUES (%s)', (nombre_C,))
        conn.commit()
        conn.close()
        return redirect(url_for('categorias'))

    return render_template('agregar_categoria.html')

# Ruta para editar categoría
@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_C = request.form['nombre_C']
        cursor.execute('UPDATE categorias SET nombre_C = %s WHERE id = %s', (nombre_C, id))
        conn.commit()
        conn.close()
        return redirect(url_for('categorias'))

    cursor.execute('SELECT * FROM categorias WHERE id = %s', (id,))
    categoria = cursor.fetchone()
    conn.close()
    return render_template('editar_categoria.html', categoria=categoria)

# Ruta para eliminar categoría
@app.route('/categorias/eliminar/<int:id>', methods=['GET'])
def eliminar_categoria(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categorias WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('categorias'))

# Ruta para ver los equipos de un usuario específico
@app.route('/usuarios/<int:id>/equipos')
def ver_equipos_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT equipos.id, equipos.nombre_E, equipos.modelo, equipos.serial, categorias.nombre_C
        FROM equipos
        JOIN categorias ON equipos.categoria_id = categorias.id
        WHERE equipos.usuario_id = %s
    """, (id,))
    equipos = cursor.fetchall()
    
    # Obtener los datos del usuario
    cursor.execute('SELECT nombre_U FROM usuarios WHERE id = %s', (id,))
    usuario = cursor.fetchone()
    
    conn.close()
    
    return render_template('ver_equipos_usuario.html', equipos=equipos, usuario=usuario)

@app.route('/reportes/usuarios')
def reportes_usuarios():
    # Conectar a la base de datos y obtener los usuarios
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.nombre_U, u.cedula_U, d.nombre_D 
        FROM usuarios u 
        LEFT JOIN departamentos d ON u.departamento_id = d.id
    """)
    usuarios = cursor.fetchall()
    conn.close()
    
    # Renderizar el template HTML para el reporte
    html = render_template('reporte_usuarios.html', usuarios=usuarios)
    
    # Convertir el HTML a PDF
    pdf = pdfkit.from_string(html, False)
    # Devolver el PDF como respuesta
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename=reportes_usuarios.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/reportes/equipos')
def reportes_equipos():
    # Conectar a la base de datos y obtener los equipos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta para obtener todos los equipos, sus categorías y los usuarios asignados
    cursor.execute("""
        SELECT e.nombre_E, e.modelo, e.serial, e.especificaciones, c.nombre_C, u.nombre_U 
        FROM equipos e 
        LEFT JOIN categorias c ON e.categoria_id = c.id
        LEFT JOIN usuarios u ON e.usuario_id = u.id
    """)
    equipos = cursor.fetchall()
    conn.close()
    
    # Renderizar el template HTML para el reporte
    html = render_template('reporte_equipos.html', equipos=equipos)
    
    # Convertir el HTML a PDF
    pdf = pdfkit.from_string(html, False)
    
    # Devolver el PDF como respuesta
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename=reportes_equipos.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/reportes/departamentos')
def reportes_departamentos():
    # Conectar a la base de datos y obtener los departamentos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_D FROM departamentos")
    departamentos = cursor.fetchall()
    conn.close()
    
    # Renderizar el template HTML para el reporte
    html = render_template('reporte_departamentos.html', departamentos=departamentos)
    
    # Convertir el HTML a PDF
    pdf = pdfkit.from_string(html, False)
    
    # Devolver el PDF como respuesta
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename=reportes_departamentos.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/usuarios/<int:id>/reportes')
def exportar_equipos_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener los equipos asignados al usuario
    cursor.execute(""" 
        SELECT equipos.nombre_E, equipos.modelo, equipos.serial, categorias.nombre_C
        FROM equipos
        JOIN categorias ON equipos.categoria_id = categorias.id
        WHERE equipos.usuario_id = %s
    """, (id,))
    equipos = cursor.fetchall()

    # Obtener los datos del usuario
    cursor.execute('SELECT nombre_U, cedula_U FROM usuarios WHERE id = %s', (id,))
    usuario = cursor.fetchone()

    conn.close()

    # Renderizar el template HTML para el PDF
    html = render_template('reporte_equipos_usuario.html', equipos=equipos, usuario=usuario)

    # Convertir el HTML a PDF
    pdf = pdfkit.from_string(html, False)

    # Devolver el PDF como respuesta
    response = make_response(pdf)
    response.headers["Content-Disposition"] = f"attachment; filename=equipos_usuario_{id}.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/')
def home_redirect():
    return redirect(url_for('home'))

# Ruta para listar categorías
@app.route('/motivos')
def motivos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM motivos')
    motivos = cursor.fetchall()
    conn.close()
    return render_template('motivos.html', motivos=motivos)

# Ruta para agregar motivo
@app.route('/motivos/agregar', methods=['GET', 'POST'])
def agregar_motivo():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_M = request.form['nombre_M']
        cursor.execute('INSERT INTO motivos (nombre_M) VALUES (%s)', (nombre_M,))
        conn.commit()
        conn.close()
        return redirect(url_for('motivos'))

    return render_template('agregar_motivo.html')

# Ruta para editar motivo
@app.route('/motivos/editar/<int:id>', methods=['GET', 'POST'])
def editar_motivo(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_M = request.form['nombre_M']
        cursor.execute('UPDATE motivos SET nombre_M = %s WHERE id = %s', (nombre_M, id))
        conn.commit()
        conn.close()
        return redirect(url_for('motivos'))

    cursor.execute('SELECT * FROM motivos WHERE id = %s', (id,))
    motivo = cursor.fetchone()
    conn.close()
    return render_template('editar_motivo.html', motivo=motivo)

# Ruta para eliminar motivos
@app.route('/motivos/eliminar/<int:id>', methods=['GET'])
def eliminar_motivo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM motivos WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('motivos'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
