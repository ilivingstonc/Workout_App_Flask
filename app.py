import models
import os
from playhouse.db_url import connect
from flask import Flask, request, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict
from resources.workouts import workout
from resources.users import user

DEBUG=True
PORT=8000

app = Flask(__name__)

######
app.secret_key = 'randomkey123'
login_manager = LoginManager()
login_manager.init_app(app)

# Decorator that will load the user object whenver we access the session
# by import currect_user from flask_login
@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None
######


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'Hello World'

CORS(workout, origins=['http://localhost:3000', 'https://workout-app-react.herokuapp.com/'], supports_credentials=True)
app.register_blueprint(workout, url_prefix='/api/v1/workouts')

CORS(user, origins=['http://localhost:3000', 'https://workout-app-react.herokuapp.com/'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/user')

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))



if __name__ == "__main__": 
    models.initialize()
    app.run(debug=DEBUG, port=PORT)