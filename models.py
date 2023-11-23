from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
db=SQLAlchemy()





#TABLES TO POPULATE USER, ADMIN, SHOWS , VENUES AND BOOKING
class Show_Venue(db.Model):
    __tablename__='show_venue'
    show_venue_id=db.Column(db.Integer,primary_key=True,autoincrement=True )
    show_id=db.Column(db.Integer, db.ForeignKey('show.show_id'))
    venue_id= db.Column(db.Integer, db.ForeignKey('venue.venue_id'))

class Booking(UserMixin,db.Model):
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=False)
    show_id = db.Column(db.Integer, nullable=False)
    venue_id=db.Column(db.Integer, nullable=False)
    seats= db.Column(db.Integer, nullable=False)

role_users = db.Table(
    'role_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class UserRating(UserMixin,db.Model):
    user_rate_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=False)
    show_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(120), nullable=False)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(50), unique=True)
    active=db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles=db.relationship('Role',secondary=role_users,backref=db.backref('users',lazy='dynamic'))
    email = db.Column(db.String,unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=None)
    report=db.Column(db.String,unique=True)

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(255))

class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    place  = db.Column(db.String(120), nullable=False)
    location = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Text, nullable=False)
    shows = db.relationship('Show',secondary='show_venue')

class Show(db.Model):
    show_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.String(120), nullable=False)
    tags = db.Column(db.String(120), nullable=False)
    show_time = db.Column(db.DateTime)
    price = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(120))
    venues = db.relationship('Venue', secondary='show_venue')

    def __init__(self, name: object, rating: object, tags: object, show_time: object, price: object,image_file: object) -> object:
        self.name = name
        self.rating = rating
        self.tags = tags
        self.show_time = show_time
        self.price = price
        self.image_file= image_file

    def json(self):
        return {'show_id': self.show_id, 'name': self.name, 'rating': self.rating, 'tags': self.tags,
                'show_time': self.show_time.isoformat(), 'price': self.price, 'image_file':self.image_file}