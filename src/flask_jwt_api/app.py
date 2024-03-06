from flask import Flask, request
from flask_restful import Api, reqparse, Resource
from flask_jwt import JWT, jwt_required
from src.flask_jwt_api.Security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'divakar'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []

class Item(Resource):
    # Put it in global scope due to multiple time use n to remove inconsistency
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="'name' can not left blank!")
    parser.add_argument('price', type=float, required=True, help="'price' can not left blank!")

    @jwt_required()
    def get(self, name):
        # item = list(filter(lambda x: x['name'] == name, items))
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 400 # == if item is not None else 400

    def post(self, name):
        req_data = request.get_json(silent=True)  # get_json(force=True) - Content Type:Application/json not required.
        name2 = req_data['name']                  # silent=True - return none when error in post json format
        price = req_data['price']
        if next(filter(lambda x: x['name'] == name2, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name2)}, 400
        item = {'name': name2, 'price': price}
        items.append(item)
        return {'Item': item}, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': f"Item {name} is deleted"}

    def put(self, name):
        req_data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == req_data['name'], items), None)
        if item is None:
            item = {'name': req_data['name'], 'price': req_data['price']}
            items.append(item)
            return {"message":"Item created", "items": items}
        else:
            item.update(req_data)
            return {"message": "Item updated", "items": items}


class ItemList(Resource):
    def get(self):
        if len(items) > 0:
            return {'item': items}, 200
        return {'item': None}, 404



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)



"""
200 - Ok, 201 - Created, 202 - Accepted, 404 - Not found and so on
"""

