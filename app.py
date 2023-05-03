import os
import io
import boto3
from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

from forms import SignUpForm

client = boto3.client(
    's3',
    # "us-east-1",
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)

s3 = boto3.resource('s3')

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

# connect_db(app)


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
    # file_path = os.path.abspath(pic)
    # data = open(pic, 'rb')
    # print('I am the data', data)
    # if put object doesnt work, use .upload_fileobj
    # TODO: change pic1 to be the username from form
    # TODO: request.files()

    # with open(pic, 'rb') as data:
    #     s3.upload_fileobj(data, os.environ['BUCKET'], 'username-pic1')
    # s3.upload_file(file_path, os.environ['BUCKET'], 'pic1')
    pic_bytes = io.BytesIO(b'pic')
    s3.upload_fileobj(pic_bytes, os.environ['BUCKET'], 'pic2' )

    return render_template('pic.html')

