import json
from flask import jsonify, Blueprint
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user
import models

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

class Register(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            user = models.User.create_user(**args)
            login_user(user)
            return marshal(user, user_fields), 201
        return jsonify({
            'error': 'Passwords do not match'
        })

class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )

    def post(self):
        args = self.reqparse.parse_args()
        user = models.User.verify_user(**args)
        if user:
            login_user(user)
            return marshal(user, user_fields), 200

class Logout(Resource):
    def post(self):
        logout_user()
        return 200

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    Register,
    '/registration'
)
api.add_resource(
    Login,
    '/login'
)
api.add_resource(
    Logout,
    '/logout'
)
