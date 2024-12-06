from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from models import db, Usuario, Libro

UPLOAD_FOLDER = 'static/uploads'
admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')


# Función para verificar si la extensión del archivo es válida
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Ruta para el dashboard
@admin_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

# Ruta para mostrar la lista de usuarios
@admin_bp.route('/users')
def users():
    usuarios = Usuario.query.all()
    return render_template('users.html', usuarios=usuarios)

# Ruta para agregar un libro (función de administrador)
@admin_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        nombre_libro = request.form['nombre_libro']
        categoria = request.form['categoria']
        url = request.form['url']

        # Verificar si se cargó una imagen
        if 'imagen' not in request.files:
            flash('No se ha seleccionado ninguna imagen', 'danger')
            return redirect(request.url)

        imagen = request.files['imagen']
        if imagen.filename == '':
            flash('No se ha seleccionado ninguna imagen', 'danger')
            return redirect(request.url)

        if imagen and allowed_file(imagen.filename):
            # Sanitiza el nombre del archivo y lo guarda en la carpeta de uploads
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(UPLOAD_FOLDER, filename)
            imagen.save(imagen_path)  # Guarda la imagen en la carpeta especificada

            # Crear el libro en la base de datos
            nuevo_libro = Libro(
                nombre_libro=nombre_libro,
                categoria=categoria,
                url=url,
                imagen=filename  # Guardamos solo el nombre del archivo en la base de datos
            )
            db.session.add(nuevo_libro)
            db.session.commit()

            flash('Libro agregado exitosamente', 'success')
            return redirect(url_for('admin.dashboard'))  # Redirige al dashboard

    return render_template('add_book.html')

