import datetime
from peewee import *
from flask_login import UserMixin

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('workouts.sqlite')

# DATABASE = SqliteDatabase('workouts.sqlite')


class User(UserMixin, Model):
    # id = PrimaryKeyField(null=False)
    email = CharField(unique=True)
    password = CharField()

    def __str__(self):
        return '<User: {}, id: {}>'.format(self.email, self.id)

    def __repr__(self):
        return '<User: {}, id: {}>'.format(self.email, self.id)

    class Meta:
        db_table = 'users'
        database = DATABASE

class Workout(Model):
    # id = PrimaryKeyField(null=False)
    title = CharField(null=False)
    activity = CharField()
    duration = CharField()
    perceived_effort = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'workouts'
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Workout], safe=True)
    print("TABLES Created")
    DATABASE.close()



