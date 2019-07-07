#coding: utf-8
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Categoria

class CategoriaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def validate_nome(self, nome):
        nome = Categoria.query.filter_by(nome=nome.data).first()
        if nome is not None:
            raise ValidationError('Esta categoria já existe!')


class DeletarForm(FlaskForm):
    lista = SelectField('Selecione', coerce=int)
    submit = SubmitField('Deletar')