import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '680b45859e009085c99d70168c812d48'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '\\static\\UPLOADS'
UPLOAD_FOLDER = APP_ROOT + UPLOAD_FOLD
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app) # db.create_all() to create tables, will have to do python, import etc
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from image_repo import routes