from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
#MAKE YOUR FORMS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user_auth_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

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
    return render_template("registration_page.html", form=form)

@app.route("/register", methods=['POST'])
def submit_registration_info():
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
        return redirect(f"/users/{user.username}")

@app.route("/login")
def login():
    """Login page"""
    if session.get("username") and session.get("email"):
        return redirect(f"/users/{session['username']}")
    form = LoginForm()
    return render_template("login_page.html", form=form)

@app.route("/login", methods=['POST'])
def submit_login_info():
    """Login post route"""
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
    return redirect(f"/users/{user.username}")

@app.route("/users/<username>")
def user_page(username):
    """The user page for the given user which is authenticated to access the page."""
    if session.get("username") == username and session.get("email"):
        user = User.query.get((session.get("username"), session.get("email")))
        feedbacks = User.feedbacks_by(db.session, session.get("username"))
        return render_template("user_page.html", user_information=user, feedbacks=feedbacks)
    return redirect("")
        
@app.route("/logout", methods=['POST'])
def logout():
    """Logout route"""
    if session.get("username") and session.get("email"):
        session.clear()
        return redirect("")
    
@app.route("/users/<username>/feedback/add")
def feedback_creation(username):
    """Feedback creation page"""
    if session.get("username") == username and session.get("email"):
        form = FeedbackForm()
        return render_template("feedback.html", form=form)
    return redirect("")

@app.route("/users/<username>/feedback/add", methods=['POST'])
def feedback_submission(username):
    """Feedback creation post route"""
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
    """User deletion post route"""
    if session.get("username") == username and session.get("email"):
        db.session.delete(db.session.query(User).filter_by(username=username).first())
        db.session.commit()
        session.clear()
        return redirect("")
    
@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def feedback_deletion(feedback_id):
    """Feedback deletion post route"""
    if session.get("username") == db.session.query(Feedback).filter(Feedback.id == feedback_id).first().username:
        feedback_to_delete = db.session.query(Feedback).filter_by(id=feedback_id).first()
        db.session.delete(feedback_to_delete)
        db.session.commit()
    return redirect("")

@app.route("/feedback/<feedback_id>/update")
def feedback_update_page(feedback_id):
    """Feedback update page"""
    if session.get("username") == db.session.query(Feedback).filter(Feedback.id == feedback_id).first().username:
        feedback_to_edit = db.session.query(Feedback).filter_by(id=feedback_id).first()
        original_feedback_data = {"title":f"{feedback_to_edit.title}", "content":f"{feedback_to_edit.content}"}
        form = FeedbackForm(data=original_feedback_data)
        return render_template("edit_feedback.html", form=form, id=feedback_id)
    
@app.route("/feedback/<feedback_id>/update", methods=["POST"])
def feedback_update(feedback_id):
    """Feedback update post route"""
    if session.get("username") == db.session.query(Feedback).filter(Feedback.id == feedback_id).first().username:
        form = FeedbackForm()
        feedback_being_editted = db.session.query(Feedback).filter_by(id=feedback_id).first()
        feedback_being_editted.title = form.title.data
        feedback_being_editted.content = form.content.data
        db.session.commit()
    return redirect("")