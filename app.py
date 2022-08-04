import bcrypt
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Bcrypt, User
from forms import Registration_Form

app = Flask(__name__)


connect_db(app)
db.create_all()

app.debug = True
app.config['SECRET_KEY'] = 'secret-key'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]= False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
toolbar = DebugToolbarExtension(app)

# Routes
@app.route("/")
def home_page():
    '''Display home page'''
    return redirect("/register")

@app.route("/register", methods = ["GET", "POST"])
def register_new_user():
    '''Get: Render registration form for new user. Post: Add newly registered user to database'''
    form = Registration_Form()

    # If a post request & valid CSRF token is present
    if form.validate_on_submit():

      username = form.username.data
      user_password= form.user_password.data
      email = form.email.data
      first_name = form.first_name.data
      last_name = form.last_name.data

    # this utilizes User class method - register() to hash the password
      new_user = User.register(username, user_password, email, first_name, last_name)

      print("*************************")
      print(new_user)

      # new_user = User(username = username, user_password = user_password, email = email, first_name = first_name, last_name = last_name )

      db.session.add(new_user)
      db.session.commit()

      return redirect("/")
    else:
      return render_template("register.html", form = form)
   


