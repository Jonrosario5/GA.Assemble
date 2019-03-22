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
    topic = ForeignKeyField(model=Topic,backref="event")
    user = ForeignKeyField(model=User,backref="usertopics")

    class Meta:
        database = DATABASE

    @classmethod
    def create_usertopic(cls,topic, user):
        cls.create(
            topic = topic,
            user= user
        )
class Event(Model):
    title = CharField(100)
    event_time = DateTimeField()
    location = CharField(200)
    details = TextField(500)
    topic = ForeignKeyField(model=Topic,backref="event")
    created_by_id = ForeignKeyField(model=User,backref="user")

    class Meta:
        database = DATABASE
    
    @classmethod
    def create_event(cls, title, event_time, location, details, topic, created_by_id):
        cls.create(
            title = title,
            event_time = event_time,
            location = location,
            details = details,
            topic = topic,
            created_by_id = created_by_id
            )
    
class User_Events(Model):
    user = ForeignKeyField(
        model=User, backref="user")
    event = ForeignKeyField(
        model=Event, backref="event")
    isHost = BooleanField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user_event(cls, user, event, isHost=True):
        cls.create(
           user = user,
           event = event,
           isHost = isHost
        )
 


            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Topic,User_Events,User_Topics,Event], safe=True)
    DATABASE.close()