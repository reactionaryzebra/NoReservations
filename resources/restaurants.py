import json
import models
from peewee import *
from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal, marshal_with, url_for)

restaurant_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'neighborhood': fields.String,
    'cuisine': fields.String,
    'url': fields.String,
    'image_url': fields.String
}


class Restaurant_List(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name supplied',
            location='json'
        )
        self.reqparse.add_argument(
            'neighborhood',
            required=True,
            help='No neighborhood supplied',
            location='json'
        )
        self.reqparse.add_argument(
            'cuisine',
            required=True,
            help='No cuisine supplied',
            location='json'
        )
        self.reqparse.add_argument(
            'url',
            required=True,
            help='No url supplied',
            location='json'
        )
        self.reqparse.add_argument(
            'image_url',
            required=False,
            help='No image url supplied',
            location='json'
        )
        super().__init__()

    def get(self):
        restaurants = [marshal(restaurant, restaurant_fields)
                       for restaurant in models.Restaurant.select()]
        return restaurants

    @marshal_with(restaurant_fields)
    def post(self):
        args = self.reqparse.parse_args()
        restaurant = models.Restaurant.create(**args)
        return (restaurant, 201)


class Single_Restaurant(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'id',
            required=True,
            help='No ID supplied',
            location='json'
        )
        super().__init__()

    @marshal_with(restaurant_fields)
    def get(self, id):
        try:
            restaurant = models.Restaurant.get_by_id(id)
        except models.Restaurant.DoesNotExist:
            raise Exception('No restaurant with that ID')
        else:
            return (restaurant, 200)


restaurants_api = Blueprint('resources.restaurants', __name__)
api = Api(restaurants_api)
api.add_resource(
    Restaurant_List,
    '/restaurants'
)
api.add_resource(
    Single_Restaurant,
    '/restaurants/<int:id>'
)
