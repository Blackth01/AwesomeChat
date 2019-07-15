#coding: utf-8
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class SalaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    senha = PasswordField('Senha')
    submit = SubmitField('Criar')

class DeletarForm(FlaskForm):
    lista = SelectField('Selecione', coerce=int)
    submit = SubmitField('Deletar')
