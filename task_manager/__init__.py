import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect # import CSRF
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment# biblioteka korzystająca z js, pozwala na konwersję na czas lokalny w templatce


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///' + os.path.join(basedir, 'task_manager.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='7660ca33d34102f065216f16'
db = SQLAlchemy(app)
csrf = CSRFProtect(app) # CSRF
bcrypt = Bcrypt(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from task_manager import routes