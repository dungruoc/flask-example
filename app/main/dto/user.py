from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'admin': fields.Boolean(required=False, description='admin', default=False),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })