"""SQLAlchemy models for Friendly."""

DEFAULT_IMG = "https://www.shutterstock.com/image-vector/clown-emoji-face-vector-600w-1306928644.jpg"


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
        primary_key=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image = db.Column(
        db.Text,
        default=DEFAULT_IMG,
    )

    hobbies = db.Column(
        db.Text,
        nullable=False,
    )

    interests = db.Column(
        db.Text,
        nullable=False,
    )

    radius = db.Column(
        db.Integer,
        nullable=False,
    )

    zip = db.Column(
        db.Text,
        nullable=False,
    )

    matches = db.relationship(
        "User",
        secondary="matches",
        primaryjoin=(Matches.user_being_liked == username),
        secondaryjoin=(Matches.user_liking == username),
        backref="matching",
    )

class Matches(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'matches'

    user_being_liked = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )

    user_liking = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )