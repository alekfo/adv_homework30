from datetime import datetime

import factory
from factory.faker import Faker

from main.app import db
from main.models import Client, ClientsParking, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = Faker("first_name")
    surname = Faker("last_name")
    credit_card = factory.Faker("credit_card_number")
    car_number = factory.Faker("license_plate")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = Faker("address")
    opened = factory.Faker("boolean", chance_of_getting_true=80)  # 80% шанс что открыта
    count_places = factory.Faker("random_int", min=10, max=100)
    count_available_places = factory.LazyAttribute(
        lambda o: o.count_places if o.opened else 0
    )
