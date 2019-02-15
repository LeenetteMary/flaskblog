from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # configz for db path in our module

# creating db instance 
db = SQLAlchemy(app)
# creating bcrypt instance for pw encryption
bcrypt = Bcrypt(app)
# creating an instance of flask_login
login_manager = LoginManager(app)
login_manager.login_view = 'login'    # passing the route function
login_manager.login_message_category = 'info'

# application initialization: importing routes
from app import routes