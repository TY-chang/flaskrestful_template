import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity

# resource is something Api can return

app = Flask(__name__)
app.secret_key = "ty"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRESQL_DATABASE_URL","sqlite:///data.db")
api = Api(app)


app.config["JWT_AUTH_URL_RULE"] = "/login"  # used to be /auth
jwt = JWT(app, authenticate, identity)
# the object -> use our app allow to authenicate user(new endpoint)
# /auth -> get name + password -> return JW token


# new resource student can be accessible via our Api
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
    # if  something import app; we dont want to runt it.
    # if the name is not main -> it is meaning we have imported the app file from elsewhere;
    # therefore, we dont need run the app
