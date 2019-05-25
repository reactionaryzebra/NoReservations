from flask import Flask
import config

port = config.PORT
debug = config.DEBUG

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=debug, port=port)
