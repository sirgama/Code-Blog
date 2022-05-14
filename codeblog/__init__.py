from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor


app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = "234345erg5dfg3s654graw^$dr"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codeblog.db'


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'minutepitcher'
app.config['MAIL_PASSWORD'] = '42625435'
mail = Mail(app)

from codeblog import views



    

