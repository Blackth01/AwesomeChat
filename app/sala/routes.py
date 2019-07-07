#coding: utf-8
from flask import render_template, flash, jsonify, request, redirect, url_for
from app import app, db
from app.sala import bp
from app.sala.forms import SalaForm, DeletarForm
from flask_login import current_user, login_required
from app.models import Usuario, Mensagem, Categoria, Sala


@bp.route('/Sala/<id_sala>/<nome_sala>')
@login_required
def sala(id_sala, nome_sala):
    if not Sala.query.filter_by(id=id_sala).first():
        flash('Esta sala não existe!')
        return redirect(url_for('main.index'))
    try:
        id = Mensagem.query.order_by(Mensagem.id.desc()).first().id
    except:
        id = 0

    sala = Sala.query.filter_by(id=id_sala).first()
    #Verifica se o usuário está banido da sala
    if(not current_user.admin and sala.isBanido(current_user.id)):
        flash('Você está banido desta sala!')
        return redirect(url_for('main.index'))

    user = Usuario()
    usuario_atual = user.query.filter_by(id=current_user.id).first()
    #Adiciona o usuário à sala
    usuario_atual.join_sala(sala)
    db.session.commit()
    #Pega as 10 últimas conversa
    conversas = Mensagem.query.filter(Mensagem.sala_id==id_sala).order_by(Mensagem.data_envio.desc()).limit(10)
    #Inverte a ordem das conversas
    conversas = conversas[::-1]
    return render_template('sala/sala.html', title='Sala', sala=sala, id_inicial=id, \
        id_sala=id_sala, conversas=conversas, user=user)


@bp.route('/Sala/Banir', methods=['POST'])
@login_required
def banir():
    sala_id = request.form['sala_id']
    usuario_id = request.form['usuario_id']
    if(not sala_id and not usuario_id):
        return 'fail'
    sala = Sala.query.filter_by(id=sala_id).first()
    usuario = Usuario.query.filter_by(id=usuario_id).first()

    if (not sala or not usuario):
        return 'fail'

    if(current_user.id != sala.admin_id and not current_user.admin):
        return 'fail'

    sala.banir(usuario)
    db.session.commit()
    return 'success'


@bp.route('/Sala/Desbanir', methods=['POST'])
@login_required
def desbanir():
    sala_id = request.form['sala_id']
    usuario_id = request.form['usuario_id']
    if(not sala_id and not usuario_id):
        return 'fail'
    sala = Sala.query.filter_by(id=sala_id).first()

    if (not sala):
        return 'fail'

    sala.desbanir(usuario_id)
    db.session.commit()
    return 'success'


@bp.route('/Sala/Listar/Banidos/<sala_id>', methods=['GET'])
@login_required
def get_banidos(sala_id):
    sala = Sala.query.filter_by(id=sala_id).first()
    if (not sala):
        return jsonify({"msg":"Esta sala não existe!"})

    if (not current_user.admin or current_user.id!=sala.admin_id):
        return jsonify({"msg":"Você não está autorizado!"})
    
    banidos = sala.banidos.all()
    i=0
    for assoc in banidos[:]:
        dicionario = {}
        dicionario['id'] = assoc.banido.id
        dicionario['nickname'] = assoc.banido.nickname
        banidos[i] = dicionario
        i+=1
    return jsonify({"banidos":banidos})


@bp.route('/Sala/Sair/<id_sala>')
@login_required
def sair_sala(id_sala):
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    usuario.leave_sala(id_sala)
    db.session.commit()
    flash('Você saiu da sala!')
    return redirect(url_for('main.index'))


@bp.route('/Sala/Cadastro/<categoria>/<cat_nome>', methods=['GET', 'POST'])
@login_required
def cad_sala(categoria, cat_nome):
    if not Categoria.query.filter_by(id=categoria).first():
        flash('A categoria selecionada não existe!')
        return redirect(url_for('main.index'))
    form = SalaForm()
    if form.validate_on_submit():
        nome_categoria = Categoria.query.filter_by(id=categoria).first().nome
        if not nome_categoria:
            flash('A categoria selecionada não existe!')
            return redirect(url_for('main.index'))
        sala = Sala(nome=form.nome.data, categoria_id=categoria, admin_id=current_user.id)
        db.session.add(sala)
        db.session.commit()
        flash('Sala criada com sucesso na categoria %s!' % nome_categoria)
        return redirect(url_for('main.index'))
    return render_template('sala/cad_sala.html', title='Cadastrar Sala', form=form, cat_nome=cat_nome)


@bp.route('/Sala/Deletar', methods=['GET', 'POST'])
@login_required
def del_sala():
    form = DeletarForm()
    if(not current_user.admin):
        salas = Sala.query.filter_by(admin_id=current_user.id).all()
    else:
        salas = Sala.query.all()
    if not salas:
        flash('Você ainda não criou nenhuma sala :(')
        return redirect(url_for('main.index'))
    form.lista.choices = [(s.id, s.nome) for s in salas]
    if form.validate_on_submit():
        sala = Sala.query.filter_by(id=form.lista.data).first()
        if (sala.admin_id == current_user.id or current_user.admin):
            db.session.delete(sala)
            db.session.commit()
            flash('Sala %s removida com sucesso!' % sala.nome)
            return redirect(url_for('main.index'))
    return render_template('sala/del_sala.html', title='Deletar Salas', form=form)