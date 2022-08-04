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
        return f"<${u.username}>,First name :${u.first_name}, ${u.last_name}, registered ${u.email} | Password : {u.user_password}."


    # @classmethod 
    # def register(cls,username, user_password, email, first_name, last_name):
    #     '''Register user with hashed passowrd and return the user.'''

    #     # bcryt.generate_password_hash() is a native flask Brypt method- this salts and hashes the userpassword. We add this to the db.
    #     hashed = bcrypt.generate_password_hash(user_password).decode("utf-8")

    # # return instance of user w/ newly haseed password
    #     return cls(username = username, user_password = hashed, email = email, first_name = first_name, last_name=last_name)


    __tablename__ = "users"

    id = db.Column(db.Text, primary_key= True, autoincrement = True)
    username = db.Column(db.String(20), nullable= False, unique = True)
    user_password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable = False, unique = True, )
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable= False)