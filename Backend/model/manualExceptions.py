from sqlalchemy import ForeignKey

from .. import db


class ManualException(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pharmacy = db.Column(db.Integer, ForeignKey("pharmacy.id"), unique=True, nullable=False)
    date = db.Column(db.Date)
