from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired('Обязательное поле')])
    password = PasswordField('Пароль', validators=[DataRequired('Обязательное поле')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
