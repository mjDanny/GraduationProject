from flask import Flask, render_template

from data import db_session
from data.stuffs import Stuffs
from data.users import Users

app = Flask(__name__)  # создали экземпляр приложения
app.config['SECRET_KEY'] = 'very secret key'


@app.route('/')
def index():
    db_sess = db_session.create_session()
    stuffs = db_sess.query(Stuffs).filter(Stuffs.id >= 1)
    return render_template('index.html',
                           title='DS',
                           stuffs=stuffs)


if __name__ == '__main__':
    db_session.global_init('db/blogs.db')  # Создание или подключение к БД
    app.run(port=5000, host='127.0.0.1')  # Запуск приложения
