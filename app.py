from flask import Flask, flash, redirect, render_template, request, session, url_for, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, validators

# Configure application
app = Flask(__name__)

class UserRegistrationForm(FORM):
    first_name = StringField("First name", validators=[validators.InputRequired()])
    uname = StringField("User name", validators=[validators.InputRequired()])
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def resgister():
    return render_template("register.html")