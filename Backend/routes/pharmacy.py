from flask import Blueprint, jsonify, request

from ..utilities import token_required
from ..model.pharmacy import Pharmacy
from .. import db

pharmacy_controller = Blueprint("pharmacy", __name__)


@pharmacy_controller.route("/pharmacies/<id>", methods=['GET'])
def get_pharmacy(id):
    item = Pharmacy.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)


@pharmacy_controller.route('/pharmacies', methods=['GET'])
@token_required
def get_Pharmacies(current_user):
    pharmacies = []
    for item in db.session.query(Pharmacy).all():
        del item.__dict__['_sa_instance_state']
        pharmacies.append(item.__dict__)
    return jsonify(pharmacies)


@pharmacy_controller.route('/pharmacies', methods=['POST'])
def create_item():
    body = request.get_json()
    db.session.add(Pharmacy(name=body['name'], email=body['email'], phone=body['phone'], place=body['place'],
                            street=body['street'], houseNumber=body['houseNumber'], postcode=body['postcode']))
    db.session.commit()
    return "item created"


@pharmacy_controller.route('/pharmacies/<id>', methods=['PUT'])
def update_item(id):
    body = request.get_json()
    db.session.query(Pharmacy).filter_by(id=id).update(
        dict(name=body['name'], email=body['email'], phone=body['phone'], place=body['place'],
             street=body['street'], houseNumber=body['houseNumber'], postcode=body['postcode']))
    db.session.commit()
    return "item updated"


@pharmacy_controller.route('/pharmacies/<id>', methods=['DELETE'])
def delete_item(id):
    db.session.query(Pharmacy).filter_by(id=id).delete()
    db.session.commit()
    return "item deleted"
