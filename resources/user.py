import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel

print(__name__)


class UserRegister(Resource):  # open endpoint to register users
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="dont give me blank!")
    parser.add_argument("password", type=str, required=True, help="dont give me blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that name already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created!"}, 201
