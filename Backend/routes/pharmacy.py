from flask import Blueprint, jsonify, request, abort

from ..utilities import token_required
from ..model.pharmacy import Pharmacy
from .. import db

pharmacy_controller = Blueprint("pharmacy", __name__)


@pharmacy_controller.route("/pharmacies/<id>", methods=['GET'])
@token_required
def get_pharmacy(id):
    item = Pharmacy.query.get(id)

    if item is None:
        abort(404)

    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)


@pharmacy_controller.route('/pharmacies', methods=['GET'])
@token_required
def get_pharmacies(current_user):
    pharmacies = []
    for item in db.session.query(Pharmacy).all():
        del item.__dict__['_sa_instance_state']
        pharmacies.append(item.__dict__)
    return jsonify(pharmacies)


@pharmacy_controller.route('/pharmacies', methods=['POST'])
@token_required
def create_item():
    body = request.get_json()

    item = db.session.query(Pharmacy).filter(Pharmacy.name == body['name']).first()

    if item is not None:
        return "pharmacy already exists"

    try:
        db.session.add(Pharmacy(name=body['name'], email=body['email'], phone=body['phone'], place=body['place'],
                                street=body['street'], houseNumber=body['houseNumber'], postcode=body['postcode']))
        db.session.commit()
    except Exception as error:
        return jsonify(str(error))

    return "pharmacy created"


@pharmacy_controller.route('/pharmacies/<id>', methods=['PUT'])
@token_required
def update_item(id):
    body = request.get_json()

    item = Pharmacy.query.get(id)

    if item is None:
        abort(404)

    try:
        db.session.query(Pharmacy).filter_by(id=id).update(
            dict(name=body['name'], email=body['email'], phone=body['phone'], place=body['place'],
                 street=body['street'], houseNumber=body['houseNumber'], postcode=body['postcode']))
        db.session.commit()
    except Exception as error:
        return jsonify(str(error))

    return "pharmacy updated"


@pharmacy_controller.route('/pharmacies/<id>', methods=['DELETE'])
@token_required
def delete_item(id):

    item = Pharmacy.query.get(id)

    if item is None:
        abort(404)

    try:
        db.session.query(Pharmacy).filter_by(id=id).delete()
        db.session.commit()
    except Exception as error:
        return jsonify(str(error))
    return "pharmacy deleted"
