from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

'''BLOG 初始檔案'''

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Caonima123fqwsfionhamio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/test?charset=utf8mb4'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'YOURMAIL'
app.config['MAIL_PASSWORD'] = 'PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
db = SQLAlchemy(app)
bycrypt=Bcrypt(app)
login_manger = LoginManager(app)
mail = Mail(app)
from blog import routes