from flask import Flask, render_template, redirect, url_for, session
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.byte_routes import byte_bp
from models import db
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos (SQLite para pruebas)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mi_base_datos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar rastreo de cambios
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mi_clave_secreta')  # Clave secreta para sesiones y cookies
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Carpeta donde se guardarán las imágenes
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}  # Extensiones permitidas para las imágenes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Máximo tamaño de imagen (16MB)
db.init_app(app)

# Registrar los blueprints
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(byte_bp, url_prefix='/byte')

@app.route('/')
def index():
    if 'user_id' not in session:
        # Redirigir al login si no está autenticado
        return redirect(url_for('byte.login'))
    # Mostrar un mensaje de bienvenida con el nombre de usuario
    return redirect(url_for('user.index'))

if __name__ == '__main__':
    # Crear las tablas de la base de datos si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # Iniciar la aplicación en modo de depuración

