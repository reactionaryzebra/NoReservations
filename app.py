from flask import Flask, g
from flask_login import LoginManager
from flask_cors import CORS
from resources.users import users_api
from resources.restaurants import restaurants_api
from resources.reservations import reservations_api
import os
import models

login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(restaurants_api, origins=[
     "http://localhost:3000"], supports_credentials=True)
CORS(reservations_api, origins=[
     "http://localhost:3000"], supports_credentials=True)
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(restaurants_api, url_prefix='/api/v1')
app.register_blueprint(reservations_api, url_prefix='/api/v1')


@app.before_request
def before_request():
    # g is global object
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/')
def index():
    return 'hello world'

if 'ON_HEROKU' in os.environ:
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=debug, port=port)
