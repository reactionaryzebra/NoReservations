import json
from flask import jsonify, Blueprint
from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user
import models

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
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


class Single_User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'id',
            required=False,
            help='No id provided',
            location=['args']
        )
        self.reqparse.add_argument(
            'password',
            required=False,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=False,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'username',
            required=False,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=False,
            help='No password provided',
            location=['form', 'json']
        )

    @marshal_with(user_fields)
    def get(self, id):
        try:
            user = models.User.get_by_id(id)
        except models.User.DoesNotExist:
            raise Exception('There is no user with this ID')
        else:
            return (user, 200)

    @marshal_with(user_fields)
    def put(self, id):
        try:
            user = models.User.get_by_id(id)
        except models.User.DoesNotExist:
            raise Exception('There is no user with this ID')
        else:
            args = self.reqparse.parse_args()
            new_args = {key: value for key,
                        value in args.items() if value is not None}
            updated_user = models.User.update_user(
                id, new_args)
            return (updated_user, 200)

    def delete(self, id):
        if models.User.delete_user(id):
            return jsonify({"message": "successfully deleted"})


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
api.add_resource(
    Single_User,
    '/<int:id>'
)
