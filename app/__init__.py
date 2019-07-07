from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login = LoginManager(app)
login.login_view = 'usuario.login'


from app.categoria import bp as categoria_bp
app.register_blueprint(categoria_bp)

from app.sala import bp as sala_bp
app.register_blueprint(sala_bp)

from app.usuario import bp as usuario_bp
app.register_blueprint(usuario_bp)

from app.main import bp as main_bp
app.register_blueprint(main_bp)


from app import models


