from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True, unique=True
                         )
    password = db.Column(db.String,
                         nullable=False,
                         )
    email = db.Column(db.String(50),
                      primary_key = True,
                      )
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                           nullable=False)
    
    #registration of user
    @classmethod
    def register(cls, username, email, first_name, last_name, pwd):
        """Register user with hashed password"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed_utf8)

    #authentication of user
    @classmethod
    def authenticate(cls, username, pwd):
        """Make sure that this user exists and password is correct"""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        
class Feedback(db.Model):
    __tablename__ = "feedback"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"), unique=True)

    user = db.relationship("User", backref="feedbacks")