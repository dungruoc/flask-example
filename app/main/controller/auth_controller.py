from flask import request
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from ..dto.auth import AuthDto
from ..util.decorator import token_required

api = AuthDto.api
user_auth = AuthDto.user_auth

parser = api.parser()
parser.add_argument('Authorization', location='headers')


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.expect(parser, validate=True)
    @token_required
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_token = request.headers.get('Authorization')
        return Auth.logout_user(auth_token=auth_token)