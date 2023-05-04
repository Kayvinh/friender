from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


class SignUpForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'username',
        validators=[Length(min=6)],
    )

    email = StringField(
        'e-mail',
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        'password',
        validators=[Length(min=6)],
    )

    hobbies = TextAreaField(
        'hobbies',
        validators=[Length(min=6), Length(max=1000)],
    )

    interests = TextAreaField(
        'interests',
        validators=[Length(min=6), Length(max=2000)],
    )

    zip = StringField(
        'zipcode',
        validators=[DataRequired()],
    )

    friend_radius = SelectField(
        'radius',
        validators=[DataRequired()],
    )

    #TODO: validate file field if pic, not txt
    image = FileField(
        '(Optional) Image',
    )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
