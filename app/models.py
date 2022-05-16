from sqlalchemy import ForeignKey
from . import db
from werkzeug.security import generate_password_hash

num = 1

class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` or some other name.
    __tablename__ = 'user_profiles'
    __table_args__ = (
        db.UniqueConstraint('email', name='unique_email'),
    )

    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    
    

    def __init__(self, email, password):
        #global num
        #self.userid = num
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        #num=num+1

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userid)  # python 2 support
        except NameError:
            return str(self.userid)  # python 3 support

    def __repr__(self):
        return '<User %r>' %  self.userid

class Reports(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` or some other name.
    __tablename__ = 'reports'

    reportid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user_profiles.userid'))
    division = db.Column(db.String)
    city = db.Column(db.String)
    crime = db.Column(db.String)
    date = db.Column(db.String)
    time = db.Column(db.String)
    details = db.Column(db.String)

    """
    def __init__(self, division, city, crime, date, time, details):
        self.userid = userid
        self.division = division
        self.city = city
        self.crime = crime
        self.date = date
        self.time = time
        self.details = details
    """