from re import I
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'price',
            type = float,
            required = True,
            help = "This field cannot be blank"
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
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message" : "An error occured while inserting data."}, 500

        # data = request.get_json()
        return item.json(), 201

    # @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('mydatabase.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return { 'message' : 'item deleted' }

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        update_item = ItemModel(name, data['price'])


        if item is None:
            try:
                update_item.insert()
            except:
                return {"message" : "An error occured while inserting data."}, 500
        else:
            try:
                update_item.update()
            except:
                return {"message" : "An error occured while inserting data."}, 500

        return update_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('mydatabase.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({"name" : row[0], "price" : row[1]})

        connection.close()
        return { "items" : items }