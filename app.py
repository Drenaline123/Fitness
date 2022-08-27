from flask import Flask, flash, redirect, render_template, request, session, url_for, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, validators, DateField, EmailField, IntegerField, SelectField, PasswordField
import re 
import datetime
import sqlite3

# Configure application
app = Flask(__name__)

regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{6,}$"

con = sqlite3.connect('fitness.db', check_same_thread=False)
db = con.cursor()
class UserRegistrationForm(Form):
    first_name = StringField("First name", validators=[validators.InputRequired(), validators.Regexp("[a-zA-Z]", flags=0, message=None)])
    uname = StringField("User name", validators=[validators.InputRequired(), validators.Length(min = 6, max = 20)])
    last_name= StringField("Last Name", validators=[validators.InputRequired(), validators.Regexp("[a-zA-Z]", flags=0, message=None)])
    dob = DateField("DOB", format='%d-%m-%Y', validators=[validators.InputRequired()])
    email= EmailField("Email", validators=[validators.InputRequired()])
    height = IntegerField("Height", validators=[validators.InputRequired()])
    weight = IntegerField("Weight", validators=[validators.InputRequired()])
    gender = SelectField("Gender", choices=["Male", "Female", "Other", "Prefer not to answer"])
    weight_unit = SelectField("Weight unit", choices=["kg", "lb"])
    height_unit = SelectField("Height unit", choices=["cm", "ft/in"])
    confirm = PasswordField("Confirm", validators=[validators.InputRequired()])
    password = PasswordField("Password", validators=[validators.InputRequired(), validators.EqualTo(confirm, message="Passwords must match"),\
    validators.Length(min= 8, max= 20, message="Password must be between 8-20 chars"), validators.Regexp(regex, flags=0, message=None)])

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
        return False
    except ValueError:
        raise True

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

    pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&!+=]).*$"
    if request.method == "POST":
        email =request.form.get('email').lower()
        db.execute( 'SELECT uname FROM users WHERE uname=?', (request.form.get('uname'),) )
        usernames = db.fetchall()
        db.execute( 'SELECT email FROM users WHERE email=?', (email,) )
        emails = db.fetchall()
        for item in request.form:
            if  not item:
                error = f'{item} not provided'
                return render_template("register.html", form=form, error=error)
                break
        result = re.findall(pattern, request.form.get('password'))
        if len(request.form.get('uname'))>20:
            error = "User name is too long"
            return render_template("register.html", form=form, error=error)

        elif len(request.form.get('uname'))<6:
            error = "User name is too short"
            return render_template("register.html", form=form, error=error)
        elif  len(usernames) !=0:
            error = "User name is in use"
            return render_template("register.html", form=form, error=error)
        elif len(emails) !=0:
            error = "Email is in use"
            return render_template("register.html", form=form, error=error)
        elif not result:
            error = 'invlaid password'
            return render_template("register.html", form=form, error=error)
        else:
            uname = request.form.get('uname')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            dob = request.form.get('dob')
            height = request.form.get('height')
            height_unit = request.form.get('height_unit')
            weight = request.form.get('weight')
            weight_unit = request.form.get('weight_unit')
            gender = request.form.get('gender')
            password = generate_password_hash(request.form.get('password'))
            db.execute('INSERT INTO users (uname, first_name, last_name, email, dob, height, height_unit, weight, weight_unit, gender, password) VALUES(?,?,?,?,?,?,?,?,?,?,?)', (uname, first_name, last_name, email, dob, height, height_unit, weight, weight_unit, gender, password))
            con.commit()
        return redirect('/login')
    return render_template("register.html", form=form)


@app.route("/hompage")
def hompage():
    return render_template("homepage.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    error = None
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("uname"):
            error = 'Please enter username'
            return render_template("login.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = 'Please enter password'
            return render_template("login.html", error=error)

        # Query database for username
        db.execute("SELECT uname, password FROM users WHERE uname = ?",(request.form.get("uname"),))
        rows = db.fetchall()

        # Ensure username exists and password is correct
        if  len(rows) != 1 or not check_password_hash(rows[0][1], request.form.get("password")):
            error = 'Invalid username/password'
            return render_template("login.html", error=error)
        # Remember which user has logged in
        else:
            session["user_id"] = rows[0][0]

        # Redirect user to home page
        return render_template("homepage.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
            return render_template("login.html")


@app.route("/create", methods=["GET", "POST"])
def create():

    db.execute( 'SELECT workout_name FROM workouts')
    workoutsr = db.fetchall()
    db.execute( 'SELECT workout_image FROM workouts')
    imagesr = db.fetchall()
    db.execute( 'SELECT workout_video FROM workouts')
    videosr = db.fetchall()
    workouts = []
    images = []
    videos = []
    for workout in workoutsr:
        workouts.append(workout[0])
    for image in imagesr:
        images.append(image[0])
    for video in videosr:
        videos.append(video[0])

    if request.method == "POST":
        if not request.form.get("workout_1"):
            error = 'Must have atelast 1 workout'
            return render_template("create.html", error=error)
        
        db.execute('INSERT INTO workouts () VALUES()', ())
        con.commit()
        return redirect("/create")
    return render_template("create.html", workouts=workouts, images=images, videos=videos)
app.run(host="0.0.0.0", port=50100, debug=True)