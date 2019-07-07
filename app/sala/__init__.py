from flask import Blueprint

bp = Blueprint('sala', __name__)

from app.sala import routes