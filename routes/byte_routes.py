from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from models import Usuario,  db

byte_bp = Blueprint('byte', __name__, template_folder='../templates/byte')

@byte_bp.route('/index')
def index():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'warning')
        return redirect(url_for('byte.login'))

    # Carga el usuario actual desde la base de datos
    user = Usuario.query.get(session['user_id'])
    return render_template('index.html', user=user)


@byte_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        user = Usuario.query.filter_by(correo=correo).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.nombre  # Opcional: guarda el nombre del usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('byte.index'))  # Redirige a la función index del blueprint 'byte'
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html')

@byte_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']

        if Usuario.query.filter_by(correo=correo).first():
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('byte.register'))

        password_hash = generate_password_hash(password)
        user = Usuario(nombre=nombre, correo=correo, password=password_hash)

        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso, ya puedes iniciar sesión', 'success')
        return redirect(url_for('byte.login'))

    return render_template('register.html')

@byte_bp.route('/logout')
def logout():
    if 'user_id' not in session:
        flash('No estás autenticado', 'danger')
        return redirect(url_for('byte.login'))

    session.pop('user_id', None)
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('byte.login'))


