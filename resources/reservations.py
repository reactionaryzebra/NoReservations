import json
import models
from peewee import *
from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal, marshal_with, url_for)

reservation_fields = {
    'restaurant_id': fields.Integer,
    'seller_id': fields.Integer,
    'current_owner_id': fields.Integer,
    'party_size': fields.Integer,
    'price': fields.Price,
    'time': fields.DateTime,
    'date': fields.DateTime,
    'closed': fields.Boolean,
    'sold': fields.Boolean
}


class Reservation_List(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'restaurant_id',
            required=True,
            help='No restaurant ID provided',
        )

    def get(self, restaurant_id):
        reservations = models.Reservation.select().where((models.Reservation.restaurant_id == restaurant_id)
                                                         & (models.Reservation.is_closed == False) & (models.Reservation.is_sold == False))
        if len(reservations) == 0:
            return jsonify({
                "message": "There are no available reservations at this restaurant"
            })
        else:
            return [marshal(reservation, reservation_fields) for reservation in reservations]


reservations_api = Blueprint('resources.reservations', __name__)
api = Api(reservations_api)
api.add_resource(Reservation_List, '/reservations/<int:restaurant_id>')
