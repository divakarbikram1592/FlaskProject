from flask import Flask, request
from flask_restful import Resource, Api, url_for

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
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

