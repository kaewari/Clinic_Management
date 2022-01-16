import twilio.rest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from flask_mysqldb import MySQL
app = Flask(__name__)

app.secret_key = '@#$%^876$%^&*OIUYTRTYUIJHG^&*((*&^$%^&*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/btl?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 10
db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(cloud_name='dt8p4xhzz',
                  api_key='286662688713995',
                  api_secret='2t2Fi7yEfzL1pWSJdFogmjCcm4E')


mysql = MySQL(app)

