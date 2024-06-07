from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    "Logs a user in"
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class RegisterForm(FlaskForm):
    "Registers a user"
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    "Handles user feedback"
    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=100)])
    content = StringField("Content", widget=TextArea(), render_kw={'rows':6, 'cols':50, 'style':'resize:none'}, validators=[InputRequired()])
    #Keep making the feedback form class, since you also need to make sure the feedback form works on the user page and stuff like that
#MAKE A FEEDBACK FORM ASAP, AS YOU NEED ONE.