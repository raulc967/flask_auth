from flask import Flask, redirect, render_template, request
from flask.globals import session
from models import db, connect_db, Users, Feedback
from forms import AddUserForm, LoginUserForm, AddFeedbackForm, UpdateFeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mochii007@localhost:5432/auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "applepie"

connect_db(app)
db.create_all()

@app.route('/')
def home():
    feedbacks = Feedback.query.all()
    return render_template('home.html', feedbacks=feedbacks)

@app.route('/register', methods = ["GET", "POST"])
def user():
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = Users(
            username = username,
            password = password,
            email = email,
            first_name = first_name,
            last_name = last_name
            )
        db.session.add(new_user)
        db.session.commit()
        session['user'] = Users.query.filter_by(username=new_user.username).first()
        return redirect("/secret")
    else:
        return render_template("createUser.html", form=form)

@app.route('/users/<username>')
def username(username):
    user = Users.query.filter_by(username=username).first()
    return render_template("secret.html", user=user)

@app.route('/users/<username>/delete')
def delete(username):
    user = Users.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def user_feedback_add(username):
    form = AddFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(
            title = title,
            content = content,
            username = username
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect('/')
    else:
        return render_template("addFeedback.html", form=form)

@app.route('/feedback/<feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    form = UpdateFeedbackForm()
    user = Feedback.query.filter_by(id=feedback_id).first()

    if form.validate_on_submit() and user.username == session['user'].username:
        user.title = form.title.data
        user.content = form.title.data
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
        return render_template("updateFeedback.html", form=form, feedback_id=feedback_id)

@app.route('/feedback/<feedback_id>/delete', methods = ['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).first()
    db.session.delete()
    db.session.commit()
    return redirect('/')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        user = Users.query.filter_by(username=username).first()
        if user and user.password == pwd:
            session['user'] = user
            return redirect("/secret")
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)