from flask import request
from flask_restplus import Resource

from ..dto.user import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, delete_a_user, save_user
from ..util.decorator import token_required, admin_token_required

api = UserDto.api
_user = UserDto.user


parser = api.parser()
parser.add_argument('Authorization', location='headers')

@api.route('/')
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @api.expect(parser)
    @token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @admin_token_required
    @api.expect(parser, _user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.expect(parser)
    @token_required
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.response(201, 'User successfully updated.')
    @api.doc('update a new user')
    @admin_token_required
    @api.expect(parser, _user, validate=False)
    def put(self, public_id):
        """Creates a new User """
        data = request.json
        return save_user(public_id, data=data)

    @api.response(404, 'User not found.')
    @api.doc('delete a user')
    @api.expect(parser)
    @admin_token_required
    @api.marshal_with(_user)
    def delete(self, public_id):
        """delete a user given its identifier"""
        print('deleting {}', public_id)
        user = delete_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user