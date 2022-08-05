from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    '''Connect to database.'''
  
    db.app = app
    db.init_app(app)


class User(db.Model):
  
    def __repr__(self):
        '''Class includes username, password, email, firs name & last name.'''
        u = self
        return f"Username: {u.username}, First name:{u.first_name}, Last name:{u.last_name}, email: {u.email} | Password: not shown."


    @classmethod 
    def register(cls,username, user_password, email, first_name, last_name):
        '''Register user with hashed passowrd.'''

        # bcryt.generate_password_hash() is a native flask Brypt method- this salts and hashes the userpassword. We add this to the db.
        hashed = bcrypt.generate_password_hash(user_password).decode("utf-8")

    # return instance of user w/ newly haseed password
        return cls(username = username, user_password = hashed, email = email, first_name = first_name, last_name=last_name)


    @classmethod
    def sign_in(cls, given_username, given_password):
      '''Validate given user and password against db for permissions.'''

      # grab username via input

      user = User.query.filter_by(username = given_username).first()

    # using flask bcrypt native method to check if db password matches given password 
      if user and bcrypt.check_password_hash(user.user_password, given_password):
          return user
      else: 
        return False


    __tablename__ = "users"
    # users sign in w/ username. So, we get from username as primary key.
    username = db.Column(db.String(20), primary_key = True)
    user_password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable = False, unique = True, )
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable= False)

    feedback = db.relationship("Feedback", backref = "users", cascade="all,delete")


class Feedback(db.Model):


    def __repr__(self):
        '''Class includes id, title, content, & username.'''
        f = self
        return f"<$Feedback id: {f.id}, column: {f.title}, content:{f.content}, Username: {f.username}>"

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable= False)
    content = db.Column(db.Text, nullable= False)
    username = db.Column(db.String, db.ForeignKey("users.username"), nullable = False)

