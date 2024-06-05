from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    "Log a user in"
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class RegisterForm(FlaskForm):
    "Register a user"
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

#MAKE A FEEDBACK FORM ASAP, AS YOU NEED ONE.