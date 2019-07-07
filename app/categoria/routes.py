#coding: utf-8
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.categoria import bp
from app.categoria.forms import CategoriaForm, DeletarForm
from flask_login import current_user, login_required
from app.models import Categoria


@bp.route('/Categoria/Cadastro', methods=['GET', 'POST'])
@login_required
def cad_categoria():
    if not current_user.admin:
        return redirect(url_for('main.index'))
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria = Categoria(nome=form.nome.data)
        db.session.add(categoria)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!')
        return redirect(url_for('main.index'))
    return render_template('categoria/categoria.html', title='Cadastro de Categorias', form=form)


@bp.route('/Categoria/Deletar', methods=['GET', 'POST'])
@login_required
def del_categoria():
    if not current_user.admin:
        flash('Você não é um administrador!')
        return redirect(url_for('main.index'))
    form = DeletarForm()
    form.lista.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    if form.validate_on_submit():
        categoria = Categoria.query.filter_by(id=form.lista.data).first()
        db.session.delete(categoria)
        db.session.commit()
        flash('A categoria %s foi removida!' % categoria.nome)
        return redirect(url_for('main.index'))
    return render_template('categoria/del_categoria.html', title='Deletar Categorias', form=form)