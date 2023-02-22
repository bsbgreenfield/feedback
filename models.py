from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hash = bcrypt.generate_password_hash(password)
        hash_utf8 = hash.decode("utf8")

        return cls(username=username, password=hash_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def login(cls, username, password):
        user = User.query.filter(User.username == username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else: 
            return False
        
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

class Feedback(db.Model):

    __tablename__  = 'feedback'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String, db.ForeignKey('users.username'))
