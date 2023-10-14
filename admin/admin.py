from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from data.image import Image
from data import db_session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [{'url': '.logout', 'title': 'Выйти'}]
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


@admin.route('/files/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    if not isLogged():
        return redirect(url_for('.login'))
    db_sess = db_session.create_session()
    file = db_sess.query(Image).get(file_id)

    db_sess.delete(file)
    db_sess.commit()

    flash('Файл удален успешно!', 'success')

    return redirect(url_for('.files'))