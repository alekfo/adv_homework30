import json
import pytest


@pytest.mark.parametrize("route", ["/clients/1", "/clients"])
def test_get_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(client) -> None:
    user_data = {
        "name": "ELENA",
        "surname": "fff",
        "credit_card": "111",
        "car_number": "234fff44",
    }
    resp = client.post(
        "/clients", data=json.dumps(user_data), content_type="application/json"
    )

    assert resp.status_code == 201


def test_create_parking(client) -> None:
    user_data = {
        "address": "on_lenina",
        "count_places": 40,
        "count_available_places": 40,
        "opened": True,
    }
    resp = client.post(
        "/parkings", data=json.dumps(user_data), content_type="application/json"
    )

    assert resp.status_code == 201


@pytest.mark.parking
def test_create_clients_parking(client) -> None:
    user_data = {"client_id": 1, "parking_id": 1}
    resp = client.post(
        "/client_parkings", data=json.dumps(user_data), content_type="application/json"
    )

    assert resp.status_code == 201


@pytest.mark.parking
def test_delete_clients_parking(client) -> None:
    user_data = {"client_id": 2, "parking_id": 1}
    add_resp = client.post(
        "/client_parkings", data=json.dumps(user_data), content_type="application/json"
    )

    user_data = {"client_id": 2, "parking_id": 1}
    delete_resp = client.delete(
        "/client_parkings", data=json.dumps(user_data), content_type="application/json"
    )

    assert delete_resp.status_code == 201


def test_app_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"
