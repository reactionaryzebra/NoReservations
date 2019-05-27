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
