#coding: utf-8
from app import db, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class SalaUsuario(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id', ondelete='CASCADE'), primary_key=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    sala = db.relationship("Sala", back_populates="usuarios")
    usuario = db.relationship("Usuario", back_populates="salas")

class SalaBanido(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id', ondelete='CASCADE'), primary_key=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    sala = db.relationship("Sala", back_populates="banidos")
    banido = db.relationship("Usuario", back_populates="bans")


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), index=True)
    senha = db.Column(db.String(120), index=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id', ondelete='CASCADE'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    mensagens = db.relationship('Mensagem', backref='sala', lazy='dynamic', cascade='all, delete')
    usuarios = db.relationship("SalaUsuario", back_populates="sala", lazy="dynamic", cascade="all, delete-orphan")
    banidos = db.relationship("SalaBanido", back_populates="sala", lazy="dynamic", cascade="all, delete-orphan")

    def check_password(self, senha):
        if (check_password_hash(self.senha, senha)):
            return True
        else:
            return False

    def set_password(self):
        self.senha = generate_password_hash(self.senha)

    def banir(self, usuario):
        if(not self.isBanido(usuario.id) and self.admin_id != usuario.id):
            assoc = SalaBanido()
            assoc.banido = usuario
            self.banidos.append(assoc)
            assoc = self.usuarios.filter_by(usuario_id=usuario.id).first()
            if (assoc):
                self.usuarios.remove(assoc)

    def desbanir(self, usuario_id):
        if(self.isBanido(usuario_id)):
            assoc = self.banidos.filter_by(usuario_id=usuario_id).first()
            self.banidos.remove(assoc)

    def isBanido(self, usuario_id):
        return self.banidos.filter_by(usuario_id=usuario_id).count()>0

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    senha = db.Column(db.String(120), index=True)
    admin = db.Column(db.Integer)
    mensagens = db.relationship('Mensagem', backref='remetente', foreign_keys="[Mensagem.usuario_id]", lazy='dynamic', cascade='all,delete')
    salas_criadas = db.relationship('Sala', backref='criador', foreign_keys='[Sala.admin_id]', lazy='dynamic', cascade='all, delete')
    salas = db.relationship('SalaUsuario', back_populates="usuario", lazy="dynamic", cascade="all, delete-orphan")
    bans = db.relationship("SalaBanido", back_populates="banido", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Usuário {}>'.format(self.nickname)

    def check_password(self, senha):
        if (check_password_hash(self.senha, senha)):
            return True
        else:
            return False

    def set_password(self):
        self.senha = generate_password_hash(self.senha)

    def join_sala(self, sala):
        if not self.entrou_sala(sala.id):
            assoc = SalaUsuario()
            assoc.sala = sala
            self.salas.append(assoc)

    def leave_sala(self, sala_id):
        if self.entrou_sala(sala_id):
            assoc = self.salas.filter_by(sala_id=sala_id).first()
            self.salas.remove(assoc)

    def update_sala(self, sala_id):
        if self.entrou_sala(sala_id):
            assoc = self.salas.filter_by(sala_id=sala_id).first()
            assoc.last_seen = datetime.utcnow()
            self.salas.append(assoc)

    def entrou_sala(self, sala_id):
        return self.salas.filter(SalaUsuario.sala_id == sala_id).count()>0

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), unique=True, index=True)
    salas = db.relationship('Sala', backref='categoria', lazy='dynamic', cascade='all, delete')

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(500), index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id', ondelete='CASCADE'), nullable=False)
    private_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Mensagem {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))
