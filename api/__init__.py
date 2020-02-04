from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import click
from flask.cli import with_appcontext
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    db.init_app(app)
    app.config['JWT_SECRET_KEY']='YOUR_SECRET_KEY'
    jwt=JWTManager(app)

    from api.Blog.blog_routes import blogs
    app.register_blueprint(blogs)

    from api.User.user_model import User

    from api.Login.login_route import login
    app.register_blueprint(login)

    from api.Tag.tag_model import Tag

    
    @click.command(name='create_admin')   
    @with_appcontext
    def create_admin():
        admin=User(email="admin_email_address",password="admin_password")
        admin.password = generate_password_hash(admin.password,'sha256',salt_length=12)
        db.session.add(admin)
        db.session.commit()

    app.cli.add_command(create_admin)

    

    return app 