import json
import models
from resources.restaurants import restaurant_fields
from resources.users import user_fields
from peewee import *
from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal, marshal_with, url_for)

reservation_fields = {
    'id': fields.Integer,
    'restaurant_id': fields.Nested(restaurant_fields),
    'seller_id': fields.Nested(user_fields),
    'current_owner_id': fields.Nested(user_fields),
    'party_size': fields.Integer,
    'price': fields.Price(2),
    'time': fields.String,
    'date': fields.String,
    'is_closed': fields.Boolean,
    'is_sold': fields.Boolean
}


class Reservation_List(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'restaurant_id',
            required=True,
            help='No restaurant ID provided',
            location=['json', 'args']
        )
        self.reqparse.add_argument(
            'seller_id',
            required=False,
            help='No seller ID provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'party_size',
            required=False,
            help='No party size provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'price',
            required=False,
            help='No price provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'time',
            required=False,
            help='No time provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'date',
            required=False,
            help='No date provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        args = self.reqparse.parse_args()
        reservations = models.Reservation.select().where(
            (models.Reservation.restaurant_id == args['restaurant_id'])
            & (models.Reservation.is_closed == False) & (models.Reservation.is_sold == False))
        if len(reservations) == 0:
            return jsonify({
                "message": "There are no available reservations at this restaurant"
            })
        else:
            return [marshal(reservation, reservation_fields) for reservation in reservations]

    def post(self):
        args = self.reqparse.parse_args()
        reservation = models.Reservation.create_reservation(**args)
        return marshal(reservation, reservation_fields), 201


class Single_Reservation(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'restaurant_id',
            required=True,
            help='No restaurant ID provided',
            location=['json', 'args']
        )
        self.reqparse.add_argument(
            'seller_id',
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'party_size',
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'price',
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'time',
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'date',
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'is_closed',
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'is_sold',
            required=False,
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(reservation_fields)
    def get(self, id):
        try:
            reservation = models.Reservation.get_by_id(id)
        except models.Reservation.DoesNotExist:
            raise Exception('No reservation exists with that ID')
        else:
            return (reservation, 200)


reservations_api = Blueprint('resources.reservations', __name__)
api = Api(reservations_api)
api.add_resource(Reservation_List, '/reservations')
api.add_resource(Single_Reservation, '/reservations/<int:id>')
