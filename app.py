import os
import io
import boto3
from dotenv import load_dotenv
import random
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from models import connect_db, User, Yes_Like, DEFAULT_IMG, db, No_Like, Match
from forms import SignUpForm, CSRFProtectForm, LoginForm

load_dotenv()

CURR_USER_KEY = "curr_user"

s3 = boto3.resource('s3')

client = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

bucket_name = os.environ["BUCKET"]

connect_db(app)


##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it."""

    g.csrf_form = CSRFProtectForm()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, re-present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            s3 = boto3.client('s3')
            pic = request.files['image']
            username = request.form['username']

            s3.upload_fileobj(
                pic,
                bucket_name,
                username,
                ExtraArgs={'ACL': 'public-read', 'ContentType': "image/jpeg"}
            )

            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image=f'https://{bucket_name}.s3.amazonaws.com/{username}'or DEFAULT_IMG,
                hobbies=form.hobbies.data,
                interests=form.interests.data,
                zip=form.zip.data,
                friend_radius=form.friend_radius.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect(f"/users/{username}")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success.
    Flash message on invalid credentials and return to login form"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    form = g.csrf_form

    if not form.validate_on_submit() or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

@app.route('/users/<username>', methods=["GET", "POST"])
def show_user(username):
    """Show user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(username)

    return render_template('users/profile.html', user=user)


@app.route('/findfriends', methods=["GET", "POST"])
def find_friends():
    """Show potential friends one at a time."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    potential_friends = g.user.potential_friends()
    friend = random.choice(potential_friends)
    user = User.query.get_or_404(friend)

    return render_template('potential.html', user=user)


@app.route('/users/thumbs_up/<username>', methods=["GET", "POST"])
def thumbs_up(username):
    """ Handle thumbs up potential friend, redirect back to findfriends """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(username)

    yes = Yes_Like(curr_user=user.username, people_who_liked_you=g.user.username)
    is_match = user.is_match(g.user.username)
    if is_match:
        match = Match(username1=user.username, username2=g.user.username)
        db.session.add_all([yes, match])

    db.session.commit()

    return redirect('/findfriends')

@app.route('/users/thumbs_down/<username>', methods=["GET", "POST"])
def thumbs_down(username):
    """ Handle thumbs down potential friend, redirect back to findfriends """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(username)
    no = No_Like(curr_user=user.username, people_who_said_no=g.user.username)

    db.session.add(no)
    db.session.commit()

    return redirect('/findfriends')


@app.route('/', methods=["GET"])
def form():
    """ Homepage """


    return render_template('base.html', user=g.user)