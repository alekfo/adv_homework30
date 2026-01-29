from typing import Any, Dict

from flask_sqlalchemy import SQLAlchemy

# from database import db
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class Client(db.Model):  # type: ignore
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=False)
    car_number = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Клиент {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):  # type: ignore
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Парковка {self.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientsParking(db.Model):  # type: ignore
    __tablename__ = "client_parking"

    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), primary_key=True)
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"), primary_key=True)
    time_in = db.Column(db.DateTime, nullable=True)
    time_out = db.Column(db.DateTime, nullable=True)

    client = db.relationship("Client", backref="client_parking")
    parking = db.relationship("Parking", backref="client_parking")

    def __repr__(self):
        return f"Клиент-парковка {self.client_id} {self.parking_id}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
