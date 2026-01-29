import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "main"))

import pytest

from main.app import create_app
from main.app import db as _db
from main.models import Client, ClientsParking, Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        clients = [
            Client(
                name="name1",
                surname="surname1",
                credit_card="credit_card1",
                car_number="car_number1",
            ),
            Client(
                name="name2",
                surname="surname2",
                credit_card="credit_card2",
                car_number="car_number2",
            ),
        ]

        parkings = [
            Parking(
                address="on pushkina",
                count_places=10,
                count_available_places=10,
                opened=True,
            ),
            Parking(
                address="busy_place",
                count_places=10,
                count_available_places=0,
                opened=True,
            ),
            Parking(
                address="closed_place",
                count_places=10,
                count_available_places=10,
                opened=False,
            ),
        ]

        _db.session.add_all(clients + parkings)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
