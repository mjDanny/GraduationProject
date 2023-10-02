from flask import Flask, render_template

app = Flask(__name__)  # создали экземпляр приложения
app.config['SECRET_KEY'] = 'very secret key'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')  # запуск приложения
