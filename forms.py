from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Optional, Length

# Pass in instance of FlaskForm to each class
class Registration_Form(FlaskForm):
    '''Creates a new instance of a registration form with the following parameters: first name, last name, email, and password.'''

    # field for completion = type of field (rendered in client), validators
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    user_password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class Sign_in(FlaskForm):
    '''Creates sign in form for user to log into application.'''

    username = StringField("Username", validators =[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class Feedback_form(FlaskForm):

    '''Formt to allow suer to create new feedback.'''

    title = StringField("Title", validators = [InputRequired(), Length(max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])
