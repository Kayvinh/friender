from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

class UserAddForm(FlaskForm):
    """Form for adding users."""

    # username = StringField(
    #     'Username',
    #     validators=[DataRequired()],
    # )

    # email = StringField(
    #     'E-mail',
    #     validators=[DataRequired(), Email()],
    # )

    # password = PasswordField(
    #     'Password',
    #     validators=[Length(min=6)],
    # )

    image = FileField(
        '(Optional) Image',
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""