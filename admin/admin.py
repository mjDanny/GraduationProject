from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from data.image import Image
from data.users import User
from data import db_session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [{'url': '.logout', 'title': 'Выйти'},
        {'url': '.stuffs', 'title': 'Stuffs'},
        {'url': '.users', 'title': 'Users'}]
db = None


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Админ-панель')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверный логин/пароль", "error")
    return render_template('admin/login.html', title='Админка')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))


# Декоратор управления таблицей stuffs
@admin.route('/stuffs')
def stuffs():
    if not isLogged():
        return redirect(url_for('.login'))
    db_sess = db_session.create_session()
    stuffs_list = db_sess.query(Image)
    return render_template('admin/stuffs.html', title='Управление товарами', menu=menu, stuffs=stuffs_list)


@admin.route('/users')
def users():
    if not isLogged():
        return redirect(url_for('.login'))
    db_sess = db_session.create_session()
    users_list = db_sess.query(User)
    return render_template('admin/users.html', title='Управление пользователями', menu=menu, users=users_list)


@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        flash('Файл не найден', 'error')
        return redirect(url_for('.files'))
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        db_sess.commit()
        flash('Информация о пользователе успешно обновлена!', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', user=user)


@admin.route('/users/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    if not isLogged():
        return redirect(url_for('.login'))
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.delete(user)
    db_sess.commit()
    flash('Пользователь успешно удалён', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/files/edit/<int:file_id>', methods=['GET', 'POST'])
def edit_file(file_id):
    db_sess = db_session.create_session()
    file = db_sess.query(Image).get(file_id)

    if not file:
        flash('Файл не найден', 'error')
        return redirect(url_for('.files'))

    if request.method == 'POST':
        # Обновляем информацию о файле на основе данных из POST-запроса
        file.name = request.form.get('name')
        file.price = request.form.get('price')
        db_sess.commit()
        flash('Информация о файле успешно обновлена!', 'success')
        return redirect(url_for('admin.stuffs'))

    return render_template('admin/edit_file.html', file=file)


@admin.route('/files/delete/<int:file_id>', methods=['GET'])  # Удаление файла из панели админа
def delete_file(file_id):
    if not isLogged():
        return redirect(url_for('.login'))
    db_sess = db_session.create_session()
    file = db_sess.query(Image).get(file_id)

    db_sess.delete(file)
    db_sess.commit()

    flash('Файл удален успешно!', 'success')

    return redirect(url_for('admin.stuffs'))
