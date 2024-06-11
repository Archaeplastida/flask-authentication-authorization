from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
#MAKE YOUR FORMS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user_auth_db" #DEFINE YOUR DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def redirect_to_home():
    """Root directory redirecting back to the register"""
    return redirect("/register")

@app.route("/register")
def register():
    """Registration page for new user"""
    if session.get("username") and session.get("email"):
        return redirect(f"/users/{session['username']}")
    form = RegisterForm()
    return render_template("registration_page.html", form=form) #FILL IN CONTENT

@app.route("/register", methods=['POST'])
def submit_registration_info(): #it needs to grab form information
    """Submits the newly created user information and lands in user profile page of newly created user"""
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        pwd = form.password.data
        user = User.register(username=name, email=email, first_name=first_name, last_name=last_name, pwd=pwd)
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username
        session["email"] = user.email
        return redirect(f"/users/{user.username}") #this needs to land on a user profile page in the future

@app.route("/login")
def login():
    """Login page"""
    if session.get("username") and session.get("email"):
        return redirect(f"/users/{session['username']}")
    form = LoginForm()
    return render_template("login_page.html", form=form) #FILL IN CONTENT

@app.route("/login", methods=['POST'])
def submit_login_info():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        user = User.authenticate(username=name, pwd=pwd)
        
        if user:
            session["username"] = user.username
            session["email"] = user.email
        else:
            return redirect("/login")
    return redirect(f"/users/{user.username}") #this needs to land on a user profile page in the future


# @app.route("/secret") #Route is to be erased in the future, since this will be a user route.
# def secret_page():
#     """Displays the page for authenticated users only"""
#     if session.get("username") and session.get("email"):
#         user = User.query.get((session.get("username"), session.get("email")))
#         return render_template("secret_page.html", user_information=user.username)
#     else:
#         return redirect("") #Make/assign a page if "secret" condition is not met

@app.route("/users/<username>") #The route for the authenticated user.
def user_page(username):
    """The user page for the given user which is authenticated to access the page."""
    if session.get("username") == username and session.get("email"):
        user = User.query.get((session.get("username"), session.get("email")))
        feedbacks = User.feedbacks_by(db.session, session.get("username"))
        return render_template("user_page.html", user_information=user, feedbacks=feedbacks)
    return redirect("") #Make/assign a page if "secret" condition is not met
        
@app.route("/logout", methods=['POST'])
def logout():
    """Logout route"""
    if session.get("username") and session.get("email"):
        session.clear()
        return redirect("")
    
@app.route("/users/<username>/feedback/add")
def feedback_creation(username):
    if session.get("username") == username and session.get("email"):
        form = FeedbackForm()
        return render_template("feedback.html", form=form)
    return redirect("")

@app.route("/users/<username>/feedback/add", methods=['POST'])
def feedback_submission(username):
    if session.get("username") == username and session.get("email"):
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f"/users/{username}")

@app.route("/users/<username>/delete", methods=["POST"])
def user_deletion(username):
    if session.get("username") == username and session.get("email"):
        db.session.delete(db.session.query(User).filter_by(username=username).first())
        db.session.commit()
        session.clear()
        return redirect("")
    
#YOU NEED TO WORK ON MAKING A WAY TO EDIT OR DELETE FEEDBACKS.