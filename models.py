import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('whatchuknow.db')

class Topic(Model):
    name = CharField(50)
    class Meta:
        database = DATABASE

    @classmethod
    def create_topic(cls,name):
        cls.create(
            name = name)


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    # user_topics = ForeignKeyField(User_Topics,backref="user_topics")
    
    class Meta:
        database = DATABASE
        
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                # user_topics = user_topics,
                is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")

# class User_Topics(Model):
#     topic = ForeignKeyField(Topic,backref="usertopics"),
#     user = ForeignKeyField(User,backref="usertopics"),
#     can_help = BooleanField(default=False)  

#     class Meta:
#         database = DATABASE


# class Event(Model):
#     title = CharField(100)
#     time = DateTimeField()
#     location = CharField(200)
#     # topics = 
#     details = TextAreaField(500)
#     attendees = ForeignKeyField(UserEvents, backref='userevents')

#     class Meta:
#         database = DATABASE

    
# class User_Events(Model):
#     user = ForeignKeyField(User, backref="user")
#     event = ForeignKeyField(Event, backref="event")
#     type = BooleanField()

#     class Meta:
#         database = DATABASE




            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Topic], safe=True)
    DATABASE.close()