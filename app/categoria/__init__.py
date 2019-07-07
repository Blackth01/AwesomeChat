from flask import Blueprint

bp = Blueprint('categoria', __name__)

from app.categoria import routes