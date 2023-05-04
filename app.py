import os
import io
import boto3
from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from models import connect_db, User, Yes_Like
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

connect_db(app)

##############################################################################
# User signup/login/logout

# test authentication in begining like warbler
# middleware tests authorization

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

    g.csrf_form = CSRFProtection()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/', methods=["GET"])
def form():
    """ Testing
    """

    form = SignUpForm()
    for bucket in s3.buckets.all():
        print(bucket.name)

    return render_template('base.html', form=form)

@app.route('/pic', methods=["POST"])
def pic():
    """ Testing
    """
    s3 = boto3.client('s3')
    print(request.form)
    pic = request.form["image"]
    print("WHAT WE WANT!!!!!",pic)


    # with open(pic, 'rb') as data:
    #     s3.upload_fileobj(data, os.environ['BUCKET'], 'username-pic1')
    # s3.upload_file(file_path, os.environ['BUCKET'], 'pic1')
    pic_bytes = io.BytesIO(b'pic')
    s3.upload_fileobj(pic_bytes, os.environ['BUCKET'], 'pic2' )

    return render_template('pic.html')

