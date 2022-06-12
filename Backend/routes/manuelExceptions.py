from flask import Blueprint

from ..model.manualExceptions import ManualException

manuelExceptions_controller = Blueprint("manuelExceptions", __name__)