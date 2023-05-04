from app import app
from models import User, db, Yes_Like, No_Like


db.drop_all()
db.create_all()

user1 = User(
    username='johndoe',
    password='password1',
    email='johndoe@gmail.com',
    image='https://example.com/images/johndoe.png',
    hobbies='reading, hiking',
    interests='history, science',
    friend_radius=10,
    zip='12345',
)
user2 = User(
    username='janedoe',
    password='password2',
    email='janedoe@gmail.com',
    image='https://example.com/images/janedoe.png',
    hobbies='swimming, traveling',
    interests='photography, art',
    friend_radius=20,
    zip='54321',
)
user3 = User(
    username='bobsmith',
    password='password3',
    email='bobsmith@gmail.com',
    image='https://example.com/images/bobsmith.png',
    hobbies='fishing, playing guitar',
    interests='music, technology',
    friend_radius=15,
    zip='67890',
)
user4 = User(
    username='sarahjones',
    password='password4',
    email='sarahjones@gmail.com',
    image='https://example.com/images/sarahjones.png',
    hobbies='yoga, cooking',
    interests='health, nutrition',
    friend_radius=25,
    zip='09876',
)
user5 = User(
    username='miketurner',
    password='password5',
    email='miketurner@gmail.com',
    image='https://example.com/images/miketurner.png',
    hobbies='running, playing basketball',
    interests='sports, movies',
    friend_radius=30,
    zip='43210',
)
user6 = User(
    username='lisasmith',
    password='password6',
    email='lisasmith@gmail.com',
    image='https://example.com/images/lisasmith.png',
    hobbies='knitting, gardening',
    interests='crafts, nature',
    friend_radius=10,
    zip='13579',
)
user7 = User(
    username='tomwilson',
    password='password7',
    email='tomwilson@gmail.com',
    image='https://example.com/images/tomwilson.png',
    hobbies='playing video games, watching TV',
    interests='technology, science fiction',
    friend_radius=20,
    zip='24680',
)
user8 = User(
    username='katejackson',
    password='password8',
    email='katejackson@gmail.com',
    image='https://example.com/images/katejackson.png',
    hobbies='skiing, snowboarding',
    interests='traveling, languages',
    friend_radius=30,
    zip='97531',
)
user9 = User(
    username='danmiller',
    password='password9',
    email='danmiller@gmail.com',
    image='https://example.com/images/danmiller.png',
    hobbies='playing guitar, writing',
    interests='music, literature',
    friend_radius=15,
    zip='86420',
)
user10 = User(
    username='amandasmith',
    password='password10',
    email='amandasmith@gmail.com',
    image='https://example.com/images/amandasmith.png',
    hobbies='dancing, painting',
    interests='art, history',
    friend_radius=25,
    zip='73190',
)

db.session.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9, user10])
try:
    db.session.commit()
except:
    db.session.rollback()
# Like section

like1 = Yes_Like(curr_user="johndoe", people_who_liked_you="janedoe")
like2 = Yes_Like(curr_user="janedoe", people_who_liked_you="johndoe")
like3 = Yes_Like(curr_user="johndoe", people_who_liked_you="amandasmith")
like4 = Yes_Like(curr_user="bobsmith", people_who_liked_you="amandasmith")

db.session.add_all([like1, like2, like3, like4])
db.session.commit()
