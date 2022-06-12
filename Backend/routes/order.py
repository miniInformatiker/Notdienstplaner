from flask import Blueprint

from ..model.order import Order

order_controller = Blueprint("order", __name__)