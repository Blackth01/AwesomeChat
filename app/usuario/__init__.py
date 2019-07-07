from flask import Blueprint

bp = Blueprint('usuario', __name__)

from app.usuario import routes