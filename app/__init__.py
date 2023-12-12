"""
Инициализация Flask-приложения
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
jwt = JWTManager(app)
api = Api(app)

api.init_app(app)

from app import models
from app import routes, api_forumpost

@login_manager.user_loader
def load_user(user_id):
    """
    Загрузка пользователя для Flask-Login.
    """
    return models.User.query.get(int(user_id))
