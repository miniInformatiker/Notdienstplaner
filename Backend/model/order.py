from sqlalchemy import ForeignKey

from .. import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pharmacy = db.Column(db.Integer, ForeignKey("pharmacy.id"), unique=True, nullable=False)
    isFirst = db.Column(db.Boolean)
