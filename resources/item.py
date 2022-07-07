import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy import Integer
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'price',
            type = float,
            required = True,
            help = "This field cannot be blank"
        )
    parser.add_argument(
            'store_id',
            type = int,
            required = True,
            help = "This field cannot be blank and every item should have a store_id"
        )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'message' : 'Item Not Found'}, 404


    def post(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return { "message" : "Item with this name {} already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message" : "An error occured while inserting data."}, 500

        # data = request.get_json()
        return item.json(), 201

    # @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return { 'message' : 'item deleted' }

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)

        if item is None:
           item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return { "items" : [ item.json() for item in items ]}