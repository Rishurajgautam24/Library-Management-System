from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_restful import Api
from flask_ckeditor import CKEditor

db = SQLAlchemy()
DB_NAME = "database.db"

ckeditor = CKEditor()


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    ckeditor.init_app(app)

    from .views import views
    from .user import user
    from .auth import auth
    from .librarian import librarian

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(librarian, url_prefix='/librarian')

    from .models import User, Section, Book
    create_database(app)

    # Api Paths
    from .api import UserAPI, SectionAPI, BookAPI
    api.add_resource(UserAPI, '/api/user/<int:id>', '/api/user')
    api.add_resource(SectionAPI, '/api/section/<int:id>', '/api/section')
    api.add_resource(BookAPI, '/api/book/<int:id>', '/api/book')
    


    login_manager=LoginManager()
    login_manager.login_view="auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        if not path.exists("LMS/"+DB_NAME):
            db.create_all()
            print("Created Database!")