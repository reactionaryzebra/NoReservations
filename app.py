from flask import Flask, g
from resources.users import users_api
import config



port = config.PORT
debug = config.DEBUG

app = Flask(__name__)

app.register_blueprint(users_api, url_prefix='/users')

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

if __name__ == '__main__':
    models.initialize()
    app.run(debug=debug, port=port)
