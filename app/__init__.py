from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_mail import Mail


from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

bootstrap=Bootstrap(app)
login= LoginManager()
login.init_app(app)
login.login_view = 'login'
login.login_message = '亲，需要登录才能查看噢！'
login.login_message_category = 'info'
mail = Mail(app)

from app.views import *