from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

token = '5f08704089afcbe6178ebc971d8c2aa9'
app.config['SECRET_KEY'] = token
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes

@app.before_first_request
def create_tables():
    database.create_all()

