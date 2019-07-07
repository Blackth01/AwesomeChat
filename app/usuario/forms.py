#coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Usuario

class LoginForm(FlaskForm):
    username = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Fazer login')

class RegisterForm(FlaskForm):
    username = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
         'Repita a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = Usuario.query.filter_by(nickname=username.data).first()
        if user is not None:
            raise ValidationError('Por favor, insira outro nickname')