from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)  # ID único
    nombre = db.Column(db.String(80), nullable=False)  # Nombre del usuario
    correo = db.Column(db.String(120), unique=True, nullable=False)  # Correo único
    password = db.Column(db.String(120), nullable=False)  # Contraseña
    is_admin = db.Column(db.Boolean, default=False)  # Indicador si es administrador o no

    def __repr__(self):
        return f"<Usuario {self.nombre} (Admin: {self.is_admin})>"

    # Método para encriptar la contraseña
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Método para verificar la contraseña
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Libro(db.Model):
    __tablename__ = 'libros'
    id_libro = db.Column(db.Integer, primary_key=True)  # ID único del libro
    nombre_libro = db.Column(db.String(30), nullable=False)  # Nombre del libro
    categoria = db.Column(db.String(30), nullable=False)  # Categoría del libro
    imagen = db.Column(db.String(60), nullable=False)  # Ruta de la imagen
    url = db.Column(db.String(100), nullable=False)  # URL del libro

    def __repr__(self):
        return f"<Libro {self.nombre_libro} (Categoría: {self.categoria})>"


class Ranking(db.Model):
    __tablename__ = 'ranking'
    id_visita = db.Column(db.Integer, primary_key=True)  # ID único de la visita
    id_libro = db.Column(db.Integer, db.ForeignKey('libros.id_libro'), nullable=False)  # ID del libro, llave foránea
    fecha_hora = db.Column(db.Date, nullable=False)  # Fecha y hora de la visita
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # ID del usuario, llave foránea

    libro = db.relationship('Libro', backref='rankings')  # Relación con la tabla libros
    usuario = db.relationship('Usuario', backref='rankings')  # Relación con la tabla usuarios

    def __repr__(self):
        return f"<Ranking LibroID: {self.id_libro}, UsuarioID: {self.id_usuario}, Fecha: {self.fecha_hora}>"
    def total_likes(self):
        return len(self.rankings)
    
class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id_comentario = db.Column(db.Integer, primary_key=True)  # ID único del comentario
    id_libro = db.Column(db.Integer, db.ForeignKey('libros.id_libro'), nullable=False)  # Relación con el libro
    comentario = db.Column(db.Text, nullable=False)  # Contenido del comentario
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Fecha y hora del comentario

    libro = db.relationship('Libro', backref='comentarios')  # Relación con el modelo Libro
