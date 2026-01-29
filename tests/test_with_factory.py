import json
import pytest
from .factories import ClientFactory, ParkingFactory
from main.models import Client, Parking, ClientsParking
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def test_create_client_with_factory(client, db):

    client_data = ClientFactory.build()

    client_dict = {
        "name": client_data.name,
        "surname": client_data.surname,
        "credit_card": client_data.credit_card,
        "car_number": client_data.car_number
    }

    initial_count = db.session.query(Client).count()

    logger.info(f'Начальное количество клиентов в базе: {initial_count}')

    resp = client.post("/clients",
                       data=json.dumps(client_dict),
                       content_type='application/json')

    assert resp.status_code == 201

    response_data = json.loads(resp.data)
    assert "id" in response_data

    final_count = db.session.query(Client).count()
    logger.info(f'Конечное количество клиентов в базе: {final_count}')
    assert final_count == initial_count + 1


def test_create_parking_with_factory(client, db):
    parking_data = ParkingFactory.build()

    parking_dict = {
        "address": parking_data.address,
        "count_places": parking_data.count_places,
        "count_available_places": parking_data.count_available_places,
        "opened": parking_data.opened
    }

    initial_count = db.session.query(Parking).count()

    resp = client.post("/parkings",
                       data=json.dumps(parking_dict),
                       content_type='application/json')

    assert resp.status_code == 201

    response_data = json.loads(resp.data)
    assert "id" in response_data

    final_count = db.session.query(Parking).count()
    assert final_count == initial_count + 1

    created_parking = db.session.query(Parking).filter(Parking.id == response_data["id"]).first()
    assert created_parking.address == parking_data.address
    assert created_parking.count_places == parking_data.count_places
    assert created_parking.count_available_places == parking_data.count_available_places
    assert created_parking.opened == parking_data.opened

    if parking_data.opened:
        assert created_parking.count_available_places == parking_data.count_places
    else:
        assert created_parking.count_available_places == 0

def test_create_clients_parking_with_factories(client, db):
    client_data = ClientFactory.build()
    client_dict = {
        "name": client_data.name,
        "surname": client_data.surname,
        "credit_card": client_data.credit_card,
        "car_number": client_data.car_number
    }
    resp = client.post("/clients",
                       data=json.dumps(client_dict),
                       content_type='application/json')
    response_data = json.loads(resp.data)
    created_clients_id = response_data["id"]

    parking_data = ParkingFactory.build()
    parking_dict = {
        "address": parking_data.address,
        "count_places": parking_data.count_places,
        "count_available_places": parking_data.count_available_places,
        "opened": parking_data.opened
    }
    resp = client.post("/parkings",
                       data=json.dumps(parking_dict),
                       content_type='application/json')
    response_data = json.loads(resp.data)
    created_parking_id = response_data["id"]

    input_data_for_test = {
        "client_id": created_clients_id,
        "parking_id": created_parking_id
    }
    add_resp = client.post("/client_parkings",
                       data=json.dumps(input_data_for_test),
                       content_type='application/json')

    assert add_resp.status_code == 201

    delete_resp = client.delete("/client_parkings",
                                data=json.dumps(input_data_for_test),
                                content_type='application/json')

    assert delete_resp.status_code == 201