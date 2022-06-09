from flask import Blueprint, jsonify

from ..model.Pharmacy import Pharmacy

pharmacy_controller = Blueprint("pharmacy", __name__)


@pharmacy_controller.route("/pharmacies/<id>", methods=['GET'])
def get_pharmacy(id):
    item = Pharmacy.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)
