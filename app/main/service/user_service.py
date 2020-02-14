import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            admin=data['admin'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_add(new_user)
        return generate_token(new_user)
        # response_object = {
        #     'status': 'success',
        #     'message': 'Successfully registered.'
        # }
        # return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def save_user(public_id, data):
    user = User.query.filter_by(public_id=public_id).first()
    print('updating', user, data)
    if user:
        if 'email' in data:
            user.email = data['email']
        if 'username' in data:
            user.username = data['username']
        if 'password' in data:
            user.password = data['password']
        print('saving', user)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully updated.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User not exists.',
        }
        return response_object, 409

def get_all_users():
    return User.query.all()

def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()

def delete_a_user(public_id):
  user = User.query.filter_by(public_id=public_id).first()
  print(user)
  if user:
    db.session.delete(user)
    db.session.commit()
    return user

def save_add(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'public_id': user.public_id,
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401