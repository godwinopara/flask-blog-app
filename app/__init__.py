from crypt import methods
from flask import Flask, flash, redirect, render_template, request, url_for
from config import Config
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from flask_migrate import Migrate
from app.models import db, User
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

# from app import routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # with app.app_context():
    db.init_app(app)
    return app


app = create_app()
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title="Home", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username Or Password")
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('index')

        flash("Login Successfull")
        return redirect(next_page)

    return render_template("login.html", title="Sign in", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("congratulation you are now a registered user")
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template("user.html", user=user, posts=posts)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your profile has been updated successfully")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
