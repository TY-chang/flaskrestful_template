from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="don't give me blank please!"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="don't give me blank store_id!"
    )

    # @app.route('/student..') replace by add_resource
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        # item = next(filter(lambda x: x["name"] == name, items), None)
        return {"message": "Not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):  # need jwt token
            return {"message": f"item named {name} exists"}, 400
            # if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": "The item exists {}".format(name)}, 400  # bad request
        # request_data = request.get_json() # if error: no attached json payload; do not have proper content-type header
        data = Item.parser.parse_args()  # request.get_json()
        item = ItemModel(
            name, data["price"], data["store_id"]
        )  # {"name": name, "price": data["price"]}
        try:
            item.save_to_db()
        except Exception as e:
            return {"messages": f"An error ocurred {e}"}, 500  # internal server error

        # you do not need content-type header; it would format into
        # basically return None

        return item.json(), 201 if item else 404  # created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Deleted"}

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price', type = float,required=True,help="don't give me blank!")
        # data = parser.parse_args()#request.get_json()
        data = Item.parser.parse_args()  # request.get_json()
        # item = ItemModel(name, data["price"])  # {"name": name, "price": data["price"]}

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # ({"items":[item.json]})
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # list(map(lambda x:x.json, ItemModel.query.all()))
