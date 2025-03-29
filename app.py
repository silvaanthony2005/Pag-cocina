from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
app.secret_key = 'tu_clave_secreta_aqui'  # Clave secreta para manejar sesiones

# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tablas si no existen
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            es_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            curso_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    ''')
    conn.commit()

    # Insertar usuario administrador si no existe
    admin = conn.execute('SELECT * FROM usuarios WHERE email = ?', ('admin@example.com',)).fetchone()
    if not admin:
        conn.execute('INSERT INTO usuarios (nombre, email, password, es_admin) VALUES (?, ?, ?, ?)',
                     ('Admin', 'admin@example.com', 'admin123', True))
        conn.commit()

    # Insertar cursos si la tabla está vacía
    cursos = conn.execute('SELECT * FROM cursos').fetchall()
    if not cursos:
        cursos_a_insertar = [
            "Fundamentos de la cocina",
            "Ingredientes y su manipulación",
            "Técnicas de cocción",
            "Preparación de platos básicos",
            "Cocina Internacional",
            "Seguridad e higiene"
        ]
        for curso in cursos_a_insertar:
            conn.execute('INSERT INTO cursos (nombre) VALUES (?)', (curso,))
        conn.commit()
    conn.close()

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de introducción
@app.route('/introduccion')
def introduccion():
    return render_template('introduccion.html')

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        usuario = conn.execute('SELECT * FROM usuarios WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if usuario:
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Correo o contraseña incorrectos')

    return render_template('login.html')
    
# Ruta para la página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if password != confirmPassword:
            return render_template('registro.html', error='Las contraseñas no coinciden')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)', (nombre, email, password))
            conn.commit()
            return redirect(url_for('login'))  # Redirigir a la página de login
        except sqlite3.IntegrityError:
            return render_template('registro.html', error='El correo ya está registrado')
        finally:
            conn.close()

    return render_template('registro.html')

# Registrar un nuevo usuario
@app.route('/registro', methods=['POST'])
def registro_post():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)', (nombre, email, password))
        conn.commit()
        return jsonify({'mensaje': 'Registro exitoso'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'mensaje': 'El correo ya está registrado'}), 400
    finally:
        conn.close()

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)  # Eliminar el ID del usuario de la sesión
    return redirect(url_for('index'))

# Ruta para verificar si el usuario está logueado
@app.route('/check_session')
def check_session():
    if 'usuario_id' in session:
        conn = get_db_connection()
        usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (session['usuario_id'],)).fetchone()
        conn.close()
        if usuario:
            return jsonify({
                'logueado': True,
                'es_admin': usuario['es_admin']  # Indicar si el usuario es admin
            })
    return jsonify({'logueado': False})

# Inscribirse en un curso
@app.route('/inscribirse', methods=['POST'])
def inscribirse():
    if 'usuario_id' not in session:
        return jsonify({'mensaje': 'Debes iniciar sesión para inscribirte', 'redirect': url_for('login')}), 401

    data = request.get_json()
    usuario_id = session['usuario_id']
    curso_id = data.get('curso_id')

    conn = get_db_connection()
    try:
        # Verificar si el curso existe
        curso = conn.execute('SELECT * FROM cursos WHERE id = ?', (curso_id,)).fetchone()
        if not curso:
            return jsonify({'mensaje': 'El curso no existe'}), 404

        # Verificar si el usuario ya está inscrito en el curso
        existe = conn.execute('SELECT * FROM inscripciones WHERE usuario_id = ? AND curso_id = ?', 
                             (usuario_id, curso_id)).fetchone()
        if existe:
            return jsonify({'mensaje': 'Ya estás inscrito en este curso'}), 400

        # Insertar la inscripción
        conn.execute('INSERT INTO inscripciones (usuario_id, curso_id) VALUES (?, ?)', 
                    (usuario_id, curso_id))
        conn.commit()
        return jsonify({'mensaje': 'Inscripción exitosa'}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'mensaje': f'Error al inscribirse: {str(e)}'}), 400
    finally:
        conn.close()

# Obtener cursos inscritos por un usuario
@app.route('/cursos-inscritos/<int:usuario_id>', methods=['GET'])
def cursos_inscritos(usuario_id):
    conn = get_db_connection()
    cursos = conn.execute('''
        SELECT cursos.nombre 
        FROM cursos 
        JOIN inscripciones ON cursos.id = inscripciones.curso_id 
        WHERE inscripciones.usuario_id = ?
    ''', (usuario_id,)).fetchall()
    conn.close()

    return jsonify([dict(curso) for curso in cursos]), 200

# Ruta para mostrar los cursos inscritos del usuario
@app.route('/mis_cursos')
def mis_cursos():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursos = conn.execute('''
        SELECT cursos.nombre 
        FROM cursos 
        JOIN inscripciones ON cursos.id = inscripciones.curso_id 
        WHERE inscripciones.usuario_id = ?
    ''', (usuario_id,)).fetchall()
    conn.close()

    return render_template('mis_cursos.html', cursos=cursos)

# Ruta para obtener el ID de un curso por su nombre
@app.route('/obtener_curso_id', methods=['POST'])
def obtener_curso_id():
    data = request.get_json()
    nombre_curso = data.get('nombre')

    conn = get_db_connection()
    curso = conn.execute('SELECT id FROM cursos WHERE nombre = ?', (nombre_curso,)).fetchone()
    conn.close()

    if curso:
        return jsonify({'curso_id': curso['id']})
    else:
        return jsonify({'error': 'Curso no encontrado'}), 404

# Ruta para la gestión de usuarios (solo accesible por administradores)
@app.route('/gestion_usuarios')
def gestion_usuarios():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (session['usuario_id'],)).fetchone()
    if not usuario or not usuario['es_admin']:
        conn.close()
        return redirect(url_for('index'))

    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('gestion_usuarios.html', usuarios=usuarios)

# Ruta para editar la información de un usuario (solo accesible por administradores)
@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM usuarios WHERE id = ?', (session['usuario_id'],)).fetchone()
    if not admin or not admin['es_admin']:
        conn.close()
        return redirect(url_for('index'))

    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,)).fetchone()
    if not usuario:
        conn.close()
        return redirect(url_for('gestion_usuarios'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        es_admin = 'es_admin' in request.form

        conn.execute('UPDATE usuarios SET nombre = ?, email = ?, es_admin = ? WHERE id = ?',
                     (nombre, email, es_admin, usuario_id))
        conn.commit()
        conn.close()
        return redirect(url_for('gestion_usuarios'))

    conn.close()
    return render_template('editar_usuario.html', usuario=usuario)

# Ruta para eliminar un usuario (solo accesible por administradores)
@app.route('/eliminar_usuario/<int:usuario_id>')
def eliminar_usuario(usuario_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM usuarios WHERE id = ?', (session['usuario_id'],)).fetchone()
    if not admin or not admin['es_admin']:
        conn.close()
        return redirect(url_for('index'))

    conn.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('gestion_usuarios'))

# Iniciar el servidor
if __name__ == '__main__':
    init_db()
    app.run(debug=True) 