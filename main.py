import os

from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename

from data import db_session
from data.image import Image
from data.stuffs import Stuffs
from data.users import User
from forms.user import RegisterForm
from forms.loginform import LoginForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__)  # создали экземпляр приложения
app.config['SECRET_KEY'] = 'very secret key'
login_manager = LoginManager()
login_manager.init_app(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        db_sess = db_session.create_session()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_image = Image(name=filename, path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db_sess.add(new_image)
            db_sess.commit()
            return redirect(url_for('index'))
        else:
            return redirect(request.url)
    return render_template('upload.html')


@login_manager.user_loader
def load_user(user_id):
    db_ses = db_session.create_session()
    return db_ses.get(User, user_id)


@app.route('/')
def index():
    found = request.args.get('substring')
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        stuffs = db_sess.query(Stuffs).filter(Stuffs.id >= 0)
    else:
        stuffs = db_sess.query(Stuffs).filter(Stuffs.id >= 0)
    return render_template('index.html',
                           title='DS',
                           stuffs=stuffs,
                           username='Авторизация')


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
        redirect('/')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            render_template('login.html', title='Авторизация',
                            message='Неверный логин или пароль',
                            form=form)
        return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init('db/blogs.db')  # Создание или подключение к БД
    app.run(port=5000, host='127.0.0.1')  # Запуск приложения
