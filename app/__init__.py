from flask import Flask, flash, redirect, render_template, url_for
from config import Config
from app.forms import LoginForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.models import db


# from app import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


app = create_app()
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

    if form.validate_on_submit():
        flash(
            f"Login request for user {form.username.data}, remember_me={form.remember_me.data}")
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign in", form=form)
