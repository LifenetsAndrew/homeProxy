from flask_restful import Resource, reqparse, marshal
import datetime
from uuid import uuid4, uuid5
from dao.models import User, Token, MarshallableModel
from dao.base import find_one, add_one

parser = reqparse.RequestParser()
parser.add_argument('login', type=str, location='json')
parser.add_argument('password', type=str, location='json')


class Login(Resource):

    @classmethod
    def generate_token(cls, user):
        username = user.login;
        now = str(datetime.datetime.now())
        token = uuid5(uuid4(), username+now)
        return str(token)


    def post(self, **kwargs):
        args = parser.parse_args();
        user = find_one(User, {'login':args['login']})
        if user and user.check_password(args['password']):
            token = Login.generate_token(user)

            new_token = Token()
            new_token.user = user
            new_token.token = token
            new_token.sequence_number = 0
            new_token.expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)
            add_one(new_token)
            return {
                'user': marshal(user.get_dict(), user.get_marshaller()),
                'token': marshal(new_token.get_dict(), new_token.get_marshaller())
            }, 200
        else:
            return {'status': 'not logined'}, 401
        return {"status":"ok"}, 200
