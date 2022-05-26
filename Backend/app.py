from datetime import datetime, timedelta

from functools import wraps
import jwt
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os

from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(80))
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150))


class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    place = db.Column(db.String(80))
    street = db.Column(db.String(80))
    houseNumber = db.Column(db.Integer)
    postcode = db.Column(db.Integer)


db.create_all()


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


@app.route('/items/<id>', methods=['GET'])
def get_pharmacy(id):
    item = Pharmacy.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)


@app.route('/pharmacies', methods=['GET'])
@token_required
def get_Pharmacies(current_user):
    items = []
    for item in db.session.query(Pharmacy).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)


@app.route('/items', methods=['POST'])
def create_item():
    body = request.get_json()
    db.session.add(Pharmacy(body['title'], body['content']))
    db.session.commit()
    return "item created"


@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    body = request.get_json()
    db.session.query(Item).filter_by(id=id).update(
        dict(title=body['title'], content=body['content']))
    db.session.commit()
    return "item updated"


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    db.session.query(Item).filter_by(id=id).delete()
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
