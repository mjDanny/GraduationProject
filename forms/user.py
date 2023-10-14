# Файл формы регистрации

# Импортируем библиотеки
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms import SubmitField
from wtforms.validators import DataRequired, Email, Length


# Создание формы регистрации
class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired('E-mail обязателен'),
                                            Email(message='E-mail был введён некорректно')])
    password = PasswordField('Пароль', validators=[DataRequired('Вы не ввели пароль'),
                                                   Length(min=6, message='Пароль слишком короткий')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired('Введите пароль повторно')])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
