from flask import Flask, flash, redirect, render_template, request, session, url_for, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, validators, DateField, EmailField, IntegerField, SelectField, PasswordField

# Configure application
app = Flask(__name__)

class UserRegistrationForm(Form):
    first_name = StringField("First name", validators=[validators.InputRequired()])
    uname = StringField("User name", validators=[validators.InputRequired()])
    last_name= StringField("Last Name", validators=[validators.InputRequired()])
    dob = DateField("DOB", validators=[validators.InputRequired()])
    email= EmailField("Email", validators=[validators.InputRequired()])
    height = IntegerField("Height", validators=[validators.InputRequired()])
    weight = IntegerField("Weight", validators=[validators.InputRequired()])
    gender = SelectField("Gender", choices=["Male", "Female", "Other", "Prefer not to answer"])
    weight_unit = SelectField("Weight unit", choices=["kg", "lb"])
    height_unit = SelectField("Height unit", choices=["cm", "ft/in"])
    password = PasswordField("Password", validators=[validators.InputRequired()])
    confirm = PasswordField("Confirm", validators=[validators.InputRequired()])

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
def register():
    form = UserRegistrationForm(request.form)
    return render_template("register.html", form=form)

app.run(host="0.0.0.0", port=50100, debug=True)