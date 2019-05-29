from peewee import *
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import config

DATABASE = PostgresqlDatabase(
    'noreservations_dev',
    user='jrez',
    password=config.DB_PASSWORD
)


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(cls.email == email).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception('User with that email already exists')

    @classmethod
    def verify_user(cls, email, password):
        email = email.lower()
        try:
            user = cls.select().where(cls.email == email).get()
        except cls.DoesNotExist:
            raise Exception('There is no account with this email address')
        else:
            if check_password_hash(user.password, password):
                return user
            else:
                raise Exception('Incorrect password')

    @classmethod
    def update_user(cls, id, args):
        cls.set_by_id(id, args)
        return cls.get_by_id(id)

    @classmethod
    def delete_user(cls, id):
        try:
            user = cls.get_by_id(id)
        except cls.DoesNotExist:
            raise Exception('There is no user with the given ID')
        else:
            user.delete_instance()
            return True


class Restaurant(Model):
    name = CharField()
    neighborhood = CharField()
    cuisine = CharField()
    url = CharField()
    image_url = CharField()
    address = CharField()
    phone = CharField()

    class Meta:
        database = DATABASE


class Reservation(Model):
    restaurant_id = ForeignKeyField(Restaurant, related_name="reservations")
    seller_id = ForeignKeyField(User, related_name="seller")
    current_owner_id = ForeignKeyField(
        User, related_name="owner")
    party_size = IntegerField()
    price = FloatField()
    date_time = DateTimeField()
    is_closed = BooleanField(default=False)
    is_sold = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_reservation(cls, restaurant_id, seller_id, party_size, price, date_time):
        reservation = cls(restaurant_id=restaurant_id, seller_id=seller_id,
                          current_owner_id=seller_id, party_size=party_size, price=price, date_time=date_time)
        reservation.save()
        return reservation

    @classmethod
    def update_reservation(cls, id, args):
        cls.set_by_id(id, args)
        return cls.get_by_id(id)

    @classmethod
    def delete_reservation(cls, id):
        try:
            reservation = cls.get_by_id(id)
        except cls.DoesNotExist:
            raise Exception('There is no reservation with the given ID')
        else:
            reservation.delete_instance()
            return True

    @classmethod
    def cleanup_old_reservations(cls):
        now = datetime.now()
        query = cls.update(is_closed=True).where(cls.date_time < now)
        query.execute()


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Restaurant, Reservation], safe=True)
    DATABASE.close()
