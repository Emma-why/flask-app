from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from models import db, Libro, Usuario, Ranking, Comentario
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from datetime import datetime


user_bp = Blueprint('user', __name__, template_folder='../templates/user')

@user_bp.route('/')
def index():
    user_id = session.get('user_id')  # Obtener el ID del usuario desde la sesión

    if not user_id:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('byte.login'))  # Redirige al inicio de sesión si no hay sesión

    # Obtener el usuario desde la base de datos
    user = Usuario.query.get(user_id)

    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('byte.login'))

    return render_template('user/index.html', user=user)



@user_bp.route('/view_books')
def view_books():
    libros = Libro.query.all()  # Suponiendo que has movido el modelo a Usuario
    return render_template('user/view_books.html', libros=libros)


@user_bp.route('/like_book/<int:libro_id>', methods=['POST'])
def like_book(libro_id):
    # Verifica si el usuario está en la sesión
    if 'user_id' not in session:
        flash("Debes iniciar sesión para dar 'Like'", 'danger')
        return redirect(url_for('user.login'))  # Redirigir al login si no hay sesión

    # Obtén el ID del usuario desde la sesión
    user_id = session['user_id']

    # Verifica si el libro existe
    libro = Libro.query.get_or_404(libro_id)

    # Busca si ya existe un registro de "like" para este libro y usuario
    existing_like = Ranking.query.filter_by(id_libro=libro_id, id_usuario=user_id).first()

    if existing_like:
        # Si ya existe el "like", lo eliminamos (quitamos el "like")
        db.session.delete(existing_like)
        db.session.commit()
        flash(f"Has retirado tu 'Like' del libro '{libro.nombre_libro}'", 'warning')
    else:
        # Si no existe, añadimos un nuevo "like"
        nuevo_like = Ranking(
            id_libro=libro.id_libro,
            id_usuario=user_id,
            fecha_hora=datetime.now()  # Registra la fecha y hora actual
        )
        db.session.add(nuevo_like)
        db.session.commit()
        flash(f"Te ha gustado el libro '{libro.nombre_libro}'", 'success')

    # Redirige a la vista de libros después de la acción
    return redirect(url_for('user.view_books'))
@user_bp.route('/book_likes', methods=['GET'])
def book_likes():
    # Consulta para contar likes por libro
    likes_by_book = (
        db.session.query(
            Libro.id_libro,
            Libro.nombre_libro,
            func.count(Ranking.id_visita).label('total_likes')
        )
        .join(Ranking, Libro.id_libro == Ranking.id_libro)
        .group_by(Libro.id_libro, Libro.nombre_libro)
        .order_by(func.count(Ranking.id_visita).desc())
        .all()
    )

    return render_template('book_likes.html', likes_by_book=likes_by_book)

@user_bp.route('/view_comments/<int:libro_id>', methods=['GET'])
def view_comments(libro_id):
    # Obtén el libro de la base de datos
    libro = Libro.query.get_or_404(libro_id)

    # Obtén los comentarios asociados al libro
    comentarios = Comentario.query.filter_by(id_libro=libro_id).all()

    return render_template('view_comments.html', libro=libro, comentarios=comentarios)

@user_bp.route('/add_comment/<int:libro_id>', methods=['POST'])
def add_comment(libro_id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para comentar.", 'danger')
        return redirect(url_for('user.login'))

    libro = Libro.query.get_or_404(libro_id)
    comentario_texto = request.form.get('comentario')
    if not comentario_texto:
        flash("El comentario no puede estar vacío.", 'danger')
        return redirect(url_for('user.view_comments', libro_id=libro_id))

    nuevo_comentario = Comentario(
        id_libro=libro.id_libro,
        comentario=comentario_texto,
        fecha_hora=datetime.utcnow()
    )
    db.session.add(nuevo_comentario)
    db.session.commit()

    flash("Comentario agregado con éxito.", 'success')
    return redirect(url_for('user.view_comments', libro_id=libro_id))
