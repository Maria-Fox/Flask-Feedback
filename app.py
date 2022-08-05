from crypt import methods
import bcrypt
from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User,Feedback
from forms import Registration_Form, Sign_in, Feedback_form

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'secret-key'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]= False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

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

    # this utilizes User class method - register() to hash the password & create new user instance
      user = User.register(username, user_password, email, first_name, last_name)

      db.session.add(user)
      db.session.commit()

      # come back and figure out session
      session["username"] = user.username

      return redirect(f"/users/{user.username}")
    else:
      return render_template("register.html", form = form)

@app.route("/login", methods = ["GET", "POST"])
def sign_in_func():
    '''Authenticate given username and password. If credentials given do not match redirect to login/register.'''

    form = Sign_in()

    if form.validate_on_submit():
        given_username = form.username.data
        given_password = form.password.data

        user = User.sign_in(given_username, given_password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            flash("Incorrect username or password. Please try again. If you do not have an account please create an account.")
            return redirect("/login")

    else:
        return render_template("sign_in.html", form=form)

@app.route("/users/<username>")
def secret(username):
    '''Direct given user to page & render acct details & feedback if unauthorized user redirect to login/signup.'''

    if "username" not in session or username != session["username"]:
        flash("Please register. If you already have an account, please sign in.")
        return redirect ("/")
    else:
          user = User.query.get_or_404(username)
          feedback = Feedback.query.all()
          return render_template("secret.html", user=user, feedback = feedback)

@app.route("/logout")
def logot_user():
    '''Remove currently logged in user from session. Redirect to register.'''

    session.pop("username")
    return redirect("/")

@app.route("/users/<username>/delete", methods = ["POST"])
def delete_user(username):
    '''Delete given user.'''

    if "username" not in session or username != session["username"]:
        flash("You must be the authorized user to delete the account. Please sign in to delete.")
        return redirect ("/")
    else: 
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()

        session["username"] = ''

        return redirect("/login")

@app.route("/users/<username>/feedback/add", methods = ["GET", "POST"])
def add_feedback(username):
    '''Get feedback form, and post for authorized user.'''

    if "username" not in session or username != session["username"]:
        flash("You must be an authorized user. Please sign in to add feedback.")
        return redirect ("/")

    form = Feedback_form()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content = content, username= username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f"/users/{new_feedback.username}")

    else:
        form = Feedback_form()
        user = User.query.get_or_404(username)
        return render_template("/feedback/addNew.html", form = form, user=user)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    '''Review or update given post if authorized user.'''

    feedback = Feedback.query.get_or_404(feedback_id) 
    user = feedback.username

    # pre populate with previous content for simple edit
    form = Feedback_form(obj=feedback.title)

    if "username" not in session or feedback.username != session["username"]:
      flash("Please sign in to review or edit feedback.")
      return redirect("/")

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        feedback.username = feedback.username

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        form = Feedback_form(obj=feedback)
        return render_template("/feedback/editFeedback.html", feedback = feedback, user=user, form=form)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_post(feedback_id):
    '''Delete given post from authorized user'''

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
      flash("Please sign in to review or edit feedback.")
      return redirect("/")
    else:
      db.session.delete(feedback)
      db.session.commit()

      return redirect(f"/users/{feedback.username}")