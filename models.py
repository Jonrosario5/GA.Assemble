import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('whatchuknow.db')

class Topic(Model):
    name = CharField(50, unique=True)
    class Meta:
        database = DATABASE

    @classmethod
    def create_topic(cls,name):
        cls.create(
            name = name)


class User(UserMixin, Model):
    username = CharField(unique=True)
    fullname = CharField()
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        
    @classmethod
    def create_user(cls, username, fullname,email, password, admin=False):
        try:
            cls.create(
                username=username,
                fullname=fullname,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")

class User_Topics(Model):
    topic = ForeignKeyField(
        model=Topic,backref="usertopics"),
    user = ForeignKeyField(
        model=User,backref="usertopics"),
    can_help = BooleanField(default=False)  

    class Meta:
        database = DATABASE

    @classmethod
    def create_usertopic(cls, topic, user, can_help=False):
        topic = topic,
        user= user,
        can_help = can_help

class Event(Model):
    title = CharField(100)
    time = DateField()
    location = CharField(200)
    details = TextField(500)

    class Meta:
        database = DATABASE

    
class User_Events(Model):
    user = ForeignKeyField(
        model=User, backref="user")
    event = ForeignKeyField(
        model=Event, backref="event")
    type = BooleanField()

    class Meta:
        database = DATABASE




            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Topic,User_Events,User_Topics,Event], safe=True)
    DATABASE.close()