from cmath import log
from flask import Flask, flash, redirect, render_template, url_for
from config import Config
from app.forms import LoginForm
from flask_migrate import Migrate
from app.models import db, User
from flask_login import LoginManager, current_user, login_user

# from app import routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
    return app


app = create_app()
login = LoginManager(app)
migrate = Migrate(app, db)


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Godwin Ahamefula Opara"}
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
    return render_template("index.html", user=user, title="Home", posts=posts)


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

        flash("Login Successfull")
        return redirect(url_for("index"))

    return render_template("login.html", title="Sign in", form=form)
