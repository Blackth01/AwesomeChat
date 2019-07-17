#coding: utf-8
from flask import render_template, flash, request, redirect, url_for
from app import db
from app.usuario import bp
from app.usuario.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Usuario
from werkzeug.urls import url_parse


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    try:
        teste = Usuario.query.filter_by(nickname='Teste').first()
        teste.nickname = 'Teste'
        db.session.commit()
    except:
        db.session.rollback()
        return redirect(url_for('usuario.login'))
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nickname=form.username.data).first()
        if usuario is None or not usuario.check_password(form.password.data):
            flash('Nome de usuário ou senha inválidos!!!')
            return redirect(url_for('usuario.login'))
        login_user(usuario, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('usuario/login.html', title='Login', form=form)

@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    try:
        teste = Usuario.query.filter_by(nickname='Teste').first()
        teste.nickname = 'Teste'
        db.session.commit()
    except:
        db.session.rollback()
        return redirect(url_for('usuario.registrar'))
    if form.validate_on_submit():
        usuario = Usuario(nickname=form.username.data, senha=form.password.data)
        usuario.set_password()
        db.session.add(usuario)
        db.session.commit()
        usuario = Usuario.query.filter_by(nickname=form.username.data).first()
        login_user(usuario)
        return redirect(url_for('main.index'))
    return render_template('usuario/registrar.html', title="Registrar", form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))