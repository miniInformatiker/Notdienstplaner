from flask import Blueprint, jsonify, request
from ..model.user import User

user_controller = Blueprint("user", __name__)


@user_controller.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        result.append(user_data)
    return jsonify({'users': result})