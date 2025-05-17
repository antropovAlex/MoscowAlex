from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from flask_wtf import FlaskForm
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class FindForm(FlaskForm):
    category = StringField('Тип дома')
    design = StringField('Дизаин дома')
    floor = StringField('Этажность')
    purpose = StringField('Назначение')
    square = StringField('Площадь дома')
    state = StringField('Состояние дома')
    submit = SubmitField('Найти')


class СreateForm(FlaskForm):
    description = TextAreaField('Описание', validators=[DataRequired()])
    address = StringField('Адресс', validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    category = StringField('Тип дома', validators=[DataRequired()])
    design = StringField('Дизаин дома', validators=[DataRequired()])
    floor = StringField('Этажность', validators=[DataRequired()])
    purpose = StringField('Назначение', validators=[DataRequired()])
    square = StringField('Площадь дома', validators=[DataRequired()])
    state = StringField('Состояние дома', validators=[DataRequired()])
    submit = SubmitField('Создать')


class RegisterForm(FlaskForm):
    surename = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    address = StringField('Адресс проживание', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
