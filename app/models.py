from datetime import date
from . import db
import enum
from werkzeug.security import generate_password_hash
from sqlalchemy import CheckConstraint


class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))

    def __init__(self,first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password,method='pbkdf2:sha256')
        # date joined


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return f"<User: {self.email}, id: {self.id} >"


class PropertyType(enum.Enum):
    house = 'House'
    apartment = 'Apartment'


class Property(db.Model):

    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(80),nullable = False)
    bedrooms =  db.Column(db.Integer,nullable = False)
    bathrooms =  db.Column(db.Integer,nullable = False)
    location =  db.Column(db.String(128),nullable = False)
    price =  db.Column(db.Numeric(12,2),nullable = False)
    type =  db.Column(db.Enum(PropertyType),nullable = False)
    description =  db.Column(db.String(2048))
    photo = db.Column(db.String(256))
    __table_args__ = (CheckConstraint(price >=0, bathrooms >= 0,bedrooms >= 0),{})

    def __init__(self,title,bedrooms,bathrooms,location,price,type,description,photo):
        self.title = title
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.location = location
        self.price = price
        self.type = type
        self.description = description
        self.photo = photo

        def __repr__(self):
            return f"<id: {self.id}, title: {self.title}, location: {self.location}>"
