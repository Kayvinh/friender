"""SQLAlchemy models for Friendly."""

from geopy.geocoders import Nominatim
from geopy.distance import distance

geolocator = Nominatim(user_agent="my_app")

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

DEFAULT_IMG = "https://www.shutterstock.com/image-vector/clown-emoji-face-vector-600w-1306928644.jpg"


bcrypt = Bcrypt()
db = SQLAlchemy()

class Match(db.Model):
    """Table for matches"""

    __tablename__ = 'matches'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )

    username1 = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
    )

    username2 = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
    )

    # time_matched = db.Column(
    #     db.DateTime,
    #     nullable=False,
    #     default=datetime.utcnow,
    # )

    # is_curr_match = db.Column(
    #     db.Boolean,
    #     nullable=False,
    #     default=True,
    # )


class Yes_Like(db.Model):
    """Table of a liker <-> liked user."""

    __tablename__ = 'yes_likes'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
    )
    # TODO: user
    curr_user = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
    )
    # TODO: change in future when brains bigger
    people_who_liked_you = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
    )


class No_Like(db.Model):
    """Table of a liker <-> not liked user."""

    __tablename__ = 'no_likes'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
    )

    curr_user = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True,
    )

    people_who_said_no = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade"),
    )


class User(db.Model):
    """User in the system.
    Contains methods for checking for potential friends and matches"""

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

    likes = db.relationship(
        "Yes_Like",
        primaryjoin=(Yes_Like.people_who_liked_you == username),
        backref="user",
    )

    def __repr__(self):
        return f"<User: {self.username}, {self.email}, {self.likes}>"

    def is_match(self, other_user):
        """ Returns Boolean for match """

        # Check if this user has liked the other user
        self_likes = Yes_Like.query.filter(
            Yes_Like.people_who_liked_you==other_user,
            Yes_Like.curr_user==self.username).first()

        # Check if the other user has liked this user
        other_user_likes = Yes_Like.query.filter(
            Yes_Like.people_who_liked_you==self.username,
            Yes_Like.curr_user==other_user).first()

        # If both users have liked each other, it's a match
        if other_user_likes and self_likes:
            return True

        return False

    def potential_friends(self):
        """Returns array of potential friends within friend radius
        TODO: Probable bug:
            Might need to call potential_friends again for the filters to
            work correctly"""

        # filter friends if they have already been matched
        friend_usernames = (
            [f.username2 for f in Match.query
             .filter(Match.username1==self.username)
                .all()
            ]) + (
            [f.username1 for f in Match.query
             .filter(Match.username2==self.username)
             .all()])

        # Filters out people who have already liked you
        users_who_liked_you = [
            like.people_who_liked_you for like in Yes_Like.query.filter(
            Yes_Like.people_who_liked_you == self.username,
            Yes_Like.curr_user != self.username)
            .all()
        ]
        # Filters out people who have already said no
        users_who_said_no = [
            dislike.people_who_said_no for dislike in No_Like.query.filter(
            No_Like.people_who_said_no == self.username,
            No_Like.curr_user != self.username)
            .all()
        ]
        # Grabs every user without your username
        users = [(u.username, u.zip) for u in User.query.all()
                 if u.username != self.username
                ]
        # Combines the previous lists with no duplicate values
        non_potential_friends = set(friend_usernames + users_who_liked_you + users_who_said_no)

        # Creates tuple of username and zip of all people not filtered out
        potential_friends_without_location = [(u[0], u[1]) for u in users if u[0] not in non_potential_friends]

        # Own users location
        location = geolocator.geocode({"postalcode": self.zip, "country": "US"})
        location_of_user = (location.latitude, location.longitude)

        # List of potential friends now filtered by location
        potential_friends_with_location = []

        for user in potential_friends_without_location:
            location = geolocator.geocode({"postalcode": user[1], "country": "US"})
            location_of_other_user = (location.latitude, location.longitude)

            if (distance(location_of_user, location_of_other_user).miles <= self.friend_radius):
                potential_friends_with_location.append(user[0])

        return potential_friends_with_location

    @classmethod
    def signup(
        cls,
        username,
        email,
        password,
        hobbies,
        interests,
        zip,
        friend_radius,
        image=DEFAULT_IMG
        ):
        """Sign up user.

        Hashes password and adds user to db.
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

# TODO: Add message model

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)