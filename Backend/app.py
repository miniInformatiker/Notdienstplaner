from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from . import db, app
from .model.Pharmacy import Pharmacy
from .routes.pharmacy import pharmacy_controller

app.register_blueprint(pharmacy_controller)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(80))
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150))


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


@app.route('/pharmacies', methods=['GET'])
@token_required
def get_Pharmacies(current_user):
    pharmacies = []
    for item in db.session.query(Pharmacy).all():
        del item.__dict__['_sa_instance_state']
        pharmacies.append(item.__dict__)
    return jsonify(pharmacies)


@app.route('/pharmacies', methods=['POST'])
def create_item():
    body = request.get_json()
    db.session.add(Pharmacy(name=body['name'], email=body['email'], phone=body['phone'], place=body['place'],
                            street=body['street'], houseNumber=body['houseNumber'], postcode=body['postcode']))
    db.session.commit()
    return "item created"


@app.route('/pharmacies/<id>', methods=['PUT'])
def update_item(id):
    body = request.get_json()
    db.session.query(Pharmacy).filter_by(id=id).update(
        dict(name=body['name'], email=body['email'], phone=body['phone'], place=body['place'],
             street=body['street'], houseNumber=body['houseNumber'], postcode=body['postcode']))
    db.session.commit()
    return "item updated"


@app.route('/pharmacies/<id>', methods=['DELETE'])
def delete_item(id):
    db.session.query(Pharmacy).filter_by(id=id).delete()
    db.session.commit()
    return "item deleted"


@app.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = User.query.filter_by(name=auth.username).first()
    print(user.password)
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})


@app.route('/users', methods=['GET'])
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


if __name__ == '__main__':
    app.run(debug=True)
