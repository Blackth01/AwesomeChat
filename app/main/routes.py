#coding: utf-8
from flask import Markup, render_template, jsonify, request
from app import app, db
from app.main import bp
from flask_login import current_user, login_required
from app.models import Usuario, Mensagem, Categoria, Sala
from datetime import datetime


@bp.route('/')
@bp.route('/index.php')
@bp.route('/index.jsf')
@login_required
def index():
    categorias = Categoria.query.all()
    return render_template('main/index.html', title='Chat', categorias=categorias)


@bp.route('/conversas', methods=['POST'])
@login_required
def conversa():
    id = request.form['id']
    sala_id = request.form['sala']
    conversas = Mensagem.query.filter(Mensagem.id>id, Mensagem.sala_id==sala_id).all()
    sala = Sala.query.filter_by(id=sala_id).first()
    resposta = ""

    if(not sala):
        return jsonify({'msg':'Esta sala não existe!'})

    if(not current_user.admin and sala.admin_id != current_user.id):
        if (sala.isBanido(current_user.id)):
            return jsonify({'mensagens': 'B', 'id': 0, 'usuarios': ''})

    i=0
    for conversa in conversas[:]:
        id = conversa.id
        #verifica se a mensagem é do próprio usuário
        if (conversa.usuario_id != current_user.id):
            if (conversa.private_id):
                #Se a mensagem privada não for para o usuário, exclui a mensagem da lista
                if(conversa.private_id != current_user.id):
                    del conversas[i]
                    continue
            dicionario = {}
            dicionario['id'] = conversa.id
            dicionario['conteudo'] = conversa.conteudo
            dicionario['remetente'] = conversa.remetente.nickname
            dicionario['data_envio'] = conversa.data_envio
            dicionario['private_id'] = conversa.private_id
            conversas[i] = dicionario
        i+=1

    usuarios = []
    for assoc in sala.usuarios:
        dicionario = {}
        dicionario['id'] = assoc.usuario.id
        dicionario['nome'] = assoc.usuario.nickname
        usuarios.append(dicionario)

    return jsonify({'mensagens': conversas, 'id': id, 'usuarios': usuarios})


@bp.route('/enviar_mensagem', methods=['POST'])
@login_required
def enviar_mensagem():
    sala_id = request.form['sala']
    sala = Sala.query.filter_by(id=sala_id).first()
    if (not sala):
        return jsonify({'id':0})

    if(not current_user.admin and sala.admin_id != current_user.id):
        if(sala.isBanido(current_user.id)):
            return jsonify({'id':0})

    mensagem = Markup(request.form['mensagem']).striptags()
    secreta = request.form['secreta']
    msg = Mensagem(conteudo=mensagem, usuario_id=current_user.id, sala_id=sala_id)
    if secreta:
        msg.private_id=secreta
    db.session.add(msg)
    db.session.flush()
    id = msg.id
    db.session.commit()
    return jsonify({'id':id})


@bp.route('/update_usuario_sala', methods=['POST'])
@login_required
def update_usuario_sala():
    sala_id = request.form['sala_id']
    usuario_id = current_user.id
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    #Atualiza o campo que indica a data da última requisição do usuário naquela sala
    usuario.update_sala(sala_id)

    #Verifica se os usuários da sala estão offline
    sala = Sala.query.filter_by(id=sala_id).first()
    if (sala):
        for assoc in sala.usuarios:
            duration = datetime.utcnow() - assoc.last_seen
            if (duration.total_seconds() > 15):
                sala.usuarios.remove(assoc)
    db.session.commit()
    return 'success'