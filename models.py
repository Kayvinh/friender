"""SQLAlchemy models for Friendly."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
DEFAULT_IMG = "https://www.shutterstock.com/image-vector/clown-emoji-face-vector-600w-1306928644.jpg"


bcrypt = Bcrypt()
db = SQLAlchemy()

# class Match(db.Model):
#     """"""
#     __tablename__ = 'matches'

#     id = db.Column(
#         db.Integer,
#         autoincrement=True,
#         primary_key=True
#     )

#     username = db

class Like(db.Model):
    """Connection of a liker <-> liked user."""

    __tablename__ = 'likes'

    curr_user = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )

    people_who_liked_you = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
    )

    people_who_said_no = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
    )

    def is_match(self):
        """ Returns Boolean for match """



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

    friend_radius = db.Column(
        db.Integer,
        nullable=False,
    )

    zip = db.Column(
        db.Text,
        nullable=False,
    )

    def potential_friends(self):
        # get usernames of people were already friends with
        # filter people we've seen, radius

        # return that list


    # matches = db.relationship(
    #     "User",
    #     secondary="matches",
    #     primaryjoin=(Like.curr_user_liked == username),
    #     secondaryjoin=(Like.like_curr_user == username),
    #     backref="matching",
    # )

    @classmethod
    def signup(cls, username, email, password, hobbies, interests, zip, friend_radius, image=DEFAULT_IMG):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image=image,
            hobbies=hobbies,
            interests=interests,
            zip=zip,
            friend_radius=friend_radius,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = User.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    # def is_followed_by(self, other_user):
    #     """Is this user followed by `other_user`?"""

    #     found_user_list = [
    #         user for user in self.followers if user == other_user]
    #     return len(found_user_list) == 1

    # def is_following(self, other_user):
    #     """Is this user following `other_use`?"""

    #     found_user_list = [
    #         user for user in self.following if user == other_user]
    #     return len(found_user_list) == 1


# class Message(db.Model):
#     """An individual message ("warble").

#     Message -> who liked it, backref="liked_by"
#     """

#     __tablename__ = 'messages'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     text = db.Column(
#         db.String(140),
#         nullable=False,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow,
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='CASCADE'),
#         nullable=False,
#     )

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)