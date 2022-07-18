import sqlite3
from models.user import UserModel
from flask_restful import Resource, Api, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type = str,
        required= True,
        help = "This field cannot be blank.")

    parser.add_argument(
        'password', 
        type = str,
        required = True,
        help  = "This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if (UserModel.find_by_username(data['username'])):
            return {"message" : "A user with this username already exists."}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return { "message" : "User created successfully."}, 201

class Home(Resource):
    def get(self):
        return { "message" : "Your app is working" }
