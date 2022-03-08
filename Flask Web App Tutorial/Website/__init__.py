from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db= SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some random string'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #this is to say to flask where my database is located
    db.init_app(app)



    #the following 4 lines are to register the blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note 

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where to go if were not logged in 
    login_manager.init_app(app) #tell the login manager which app we are using

    @login_manager.user_loader
    def load_user(id): # this is telling flask how we load a user
        return User.query.get(int(id))

    return app

def create_database(app): #it will check if the database exists, and if not to create it 
    if not path.exists('Website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Datavase!')

