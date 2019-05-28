from peewee import *
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('reservations.sqlite')


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


class Restaurant(Model):
    name = CharField()
    neighborhood = CharField()
    cuisine = CharField()
    url = CharField()
    image_url = CharField()

    class Meta:
        database = DATABASE


class Reservation(Model):
    restaurant_id = ForeignKeyField(Restaurant, related_name="reservations")
    seller_id = ForeignKeyField(User, related_name="seller")
    current_owner_id = ForeignKeyField(
        User, related_name="owner")
    party_size = IntegerField()
    price = FloatField()
    time = TimeField()
    date = DateField()
    is_closed = BooleanField(default=False)
    is_sold = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_reservation(cls, restaurant_id, seller_id, party_size, price, time, date):
        reservation = cls(restaurant_id=restaurant_id, seller_id=seller_id,
                          current_owner_id=seller_id, party_size=party_size, price=price, time=time, date=date)
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


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Restaurant, Reservation], safe=True)
    DATABASE.close()
