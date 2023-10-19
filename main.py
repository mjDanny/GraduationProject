import os
import zipfile
from flask import Flask, render_template, redirect, request, url_for, flash, send_file
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_paginate import Pagination
from werkzeug.utils import secure_filename

from data import db_session
from data.image import Image
from data.stuffs import Stuffs
from data.users import User
from data.zip import Zip

from forms.user import RegisterForm
from forms.loginform import LoginForm

from admin.admin import admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very secret key'
app.register_blueprint(admin, url_prefix='/admin')
login_manager = LoginManager()
login_manager.init_app(app)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['UPLOAD_ZIP_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'zip', 'jpg', 'jpeg'}
PERPAGE = 8


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@login_manager.user_loader
def load_user(user_id):
    db_ses = db_session.create_session()
    return db_ses.get(User, user_id)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    if request.method == 'POST':
        pass
    offset = PERPAGE * (page - 1)
    total = 0
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        stuffs = db_sess.query(Stuffs).filter(Stuffs.id >= 0)
        image = db_sess.query(Image).filter(Image.id >= 0)
    else:
        stuffs = db_sess.query(Stuffs).filter(Stuffs.id >= 0)
        image = db_sess.query(Image).filter(Image.id >= 0)
    try:
        total = image.count()
    except:
        total = 0

    # Настройка пагинации
    pagination = Pagination(page=page, total=total, per_page=PERPAGE, search=False, bs_version=3)

    return render_template('index.html',
                           title='DS',
                           stuffs=stuffs,
                           image=image,
                           data=image[offset: offset + PERPAGE],
                           per_page=PERPAGE,
                           pagination=pagination,
                           username='Авторизация')


@app.route('/dialog', methods=['GET', 'POST'])
def process_dialog():
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        if user_input == 'Привет':
            response = 'Привет! Как я могу помочь тебе? 😊'
        elif user_input == 'Пока':
            response = 'До свидания! Удачи! 👋'
        elif user_input == 'Как дела?':
            response = 'Всё хорошо, пишу дипломный проект :)'
        else:
            response = 'Не понимаю, что ты имеешь в виду. 😕'

        return render_template('response.html', response=response)

    return render_template('template.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        price = request.form['price']
        name = request.form['name']
        if file.filename == '':
            return redirect(request.url)
        db_sess = db_session.create_session()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_image = Image(name=name, price=price, path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db_sess.add(new_image)
            db_sess.commit()
            return redirect(url_for('index'))
        else:
            return redirect(request.url)
    return render_template('upload.html')


@app.route('/zip', methods=['GET', 'POST'])
def zip_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        name = request.form['name']
        if file.filename == '':
            return redirect(request.url)
        db_sess = db_session.create_session()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_ZIP_FOLDER'], filename))
            new_zip = Zip(name=name, path=os.path.join(app.config['UPLOAD_ZIP_FOLDER'], filename))
            db_sess.add(new_zip)
            db_sess.commit()

            # Распаковка zip архива
            with zipfile.ZipFile(os.path.join(app.config['UPLOAD_ZIP_FOLDER'], filename), 'r') as zip_ref:
                extracted_path = os.path.join(app.config['UPLOAD_ZIP_FOLDER'], 'extracted')
                zip_ref.extractall(extracted_path)

            return redirect('index')

        else:
            return redirect(request.url)
    return render_template('zip.html')


@app.route('/download/<int:id>')
@login_required
def file_download(id):
    # Получаем файл из базы данных по id
    db_sess = db_session.create_session()
    item = db_sess.query(Image).filter(Image.id == id).first()

    if not item:
        return "Файл не найден"

    # Определяем путь к файлу
    full_path = os.path.join(app.root_path, item.path)

    # Отправляем файл для скачивания
    return send_file(full_path, as_attachment=True)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Такой пользователь уже существует')
        user = User(name=form.name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            else:
                flash('Неверный логин или пароль', 'error')

        return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init('db/blogs.db')  # Создание или подключение к БД
    app.run(port=5000, host='127.0.0.1')  # Запуск приложения
