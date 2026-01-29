from flask import Flask, request, jsonify
from typing import List

# from database import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from models import Client, Parking, ClientsParking, db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hw29.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET"])
    def get_all_clients():
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [i_client.to_json() for i_client in clients]
        return jsonify(clients_list), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_by_id(client_id):
        client: Client = (
            db.session.query(Client).filter(Client.id == client_id).one_or_none()
        )
        if client:
            return jsonify(client.to_json()), 200
        return jsonify({"error": "Клиента с таким айди не существует"}), 404

    @app.route("/clients", methods=["POST"])
    def create_client():
        data = request.get_json()
        name = data.get("name")
        surname = data.get("surname")
        credit_card = data.get("credit_card")
        car_number = data.get("car_number")

        new_client = Client(
            name=name, surname=surname, credit_card=credit_card, car_number=car_number
        )

        db.session.add(new_client)
        db.session.commit()
        return new_client.to_json(), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data = request.get_json()
        address = data.get("address")
        count_places = data.get("count_places")
        count_available_places = data.get("count_available_places")
        opened = data.get("opened")

        new_parking = Parking(
            address=address,
            count_places=count_places,
            count_available_places=count_available_places,
            opened=True if opened is None else opened,
        )

        db.session.add(new_parking)
        db.session.commit()
        return new_parking.to_json(), 201

    @app.route("/client_parkings", methods=["POST"])
    def create_client_parkings():
        try:
            data = request.get_json()
            client_id = data.get("client_id")
            parking_id = data.get("parking_id")
            client: Client = (
                db.session.query(Client).filter(Client.id == client_id).one_or_none()
            )
            parking: Parking = (
                db.session.query(Parking).filter(Parking.id == parking_id).one_or_none()
            )

            if not client:
                return jsonify({"error": "Клиента с таким айди не существует"}), 404
            if not parking:
                return jsonify({"error": "Парковки с таким айди не существует"}), 404
            if not parking.opened:
                return jsonify({"error": "Парковка закрыта"}), 451

            old_count_available_places = parking.count_available_places

            if old_count_available_places == 0:
                return jsonify({"error": "Нет свободных мест"}), 451
            new_client_parking = ClientsParking(
                client_id=client_id, parking_id=parking_id, time_in=datetime.now()
            )
            db.session.add(new_client_parking)
            parking.count_available_places = old_count_available_places - 1
            db.session.commit()

            return new_client_parking.to_json(), 201
        except IntegrityError:
            return jsonify({"error": "Такое бронирование уже существует"}), 404

    @app.route("/client_parkings", methods=["DELETE"])
    def delete_client_parkings():
        data = request.get_json()
        client_id = data.get("client_id")
        parking_id = data.get("parking_id")
        parking: Parking = (
            db.session.query(Parking).filter(Parking.id == parking_id).one_or_none()
        )
        client_parking: ClientsParking = (
            db.session.query(ClientsParking)
            .filter(
                ClientsParking.client_id == client_id,
                ClientsParking.parking_id == parking_id,
            )
            .one_or_none()
        )
        old_count_available_places = parking.count_available_places
        if not client_parking:
            return (
                jsonify(
                    {"error": "Такого бронирования не существует, проверьте данные"}
                ),
                404,
            )

        client_parking.time_out = datetime.now()

        parking.count_available_places = old_count_available_places + 1
        db.session.commit()

        return client_parking.to_json(), 201

    return app


if __name__ == "__main__":
    print("Hello_world")
    app = create_app()
    app.run()
