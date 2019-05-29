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
    'date': fields.String,
    'time': fields.String,
    'is_closed': fields.Boolean,
    'is_sold': fields.Boolean
}


class Reservation_List(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'user_id',
            required=False,
            help='No user ID provided',
            location=['json', 'args']
        )
        self.reqparse.add_argument(
            'restaurant_id',
            required=False,
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
            'date',
            required=False,
            help='No time provided',
            location=['json', 'args']
        )
        self.reqparse.add_argument(
            'time',
            required=False,
            help='No time provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        models.Reservation.cleanup_old_reservations()
        args = self.reqparse.parse_args()
        if args['restaurant_id'] and args['date']:
            reservations = models.Reservation.select().where(
                (models.Reservation.date == args['date']) &
                (models.Reservation.restaurant_id == args['restaurant_id'])
                & (models.Reservation.is_closed == False) & (models.Reservation.is_sold == False))
            if len(reservations) == 0:
                return jsonify({
                    "message": "There are no available reservations at this restaurant"
                })
            else:
                return [marshal(reservation, reservation_fields) for reservation in reservations]
        elif args['restaurant_id']:
            reservations = models.Reservation.select().where(
                (models.Reservation.restaurant_id == args['restaurant_id'])
                & (models.Reservation.is_closed == False) & (models.Reservation.is_sold == False))
            if len(reservations) == 0:
                return jsonify({
                    "message": "There are no available reservations at this restaurant"
                })
            else:
                return [marshal(reservation, reservation_fields) for reservation in reservations]
        elif args['user_id']:
            reservations = models.Reservation.select().where(
                (models.Reservation.seller_id ==
                 args['user_id']) | (models.Reservation.current_owner_id == args['user_id']))
            if len(reservations) == 0:
                return jsonify({"message": "This user has no reservations"})
            else:
                return [marshal(reservation, reservation_fields) for reservation in reservations]

    def post(self):
        args = self.reqparse.parse_args()
        new_args = {key: value for key,
                    value in args.items() if value is not None}
        reservation = models.Reservation.create_reservation(**new_args)
        return marshal(reservation, reservation_fields), 201


class Single_Reservation(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'restaurant_id',
            required=False,
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
            'date',
            required=False,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'time',
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

    @marshal_with(reservation_fields)
    def put(self, id):
        try:
            reservation = models.Reservation.get_by_id(id)
        except models.Reservation.DoesNotExist:
            raise Exception('No reservation exists with that ID')
        else:
            args = self.reqparse.parse_args()
            new_args = {key: value for key,
                        value in args.items() if value is not None}
            updated_reservation = models.Reservation.update_reservation(
                id, new_args)
            return (updated_reservation, 200)

    def delete(self, id):
        if models.Reservation.delete_reservation(id):
            return jsonify({"message": "successfully deleted"})


reservations_api = Blueprint('resources.reservations', __name__)
api = Api(reservations_api)
api.add_resource(Reservation_List, '/reservations')
api.add_resource(Single_Reservation, '/reservations/<int:id>')
