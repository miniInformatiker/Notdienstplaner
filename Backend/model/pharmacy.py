from .. import db


class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    place = db.Column(db.String(80))
    street = db.Column(db.String(80))
    houseNumber = db.Column(db.Integer)
    postcode = db.Column(db.Integer)