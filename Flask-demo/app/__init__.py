from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app import config

app = Flask(__name__)
app.config.from_object(config.Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes
