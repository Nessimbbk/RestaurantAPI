from flask import Flask, app
from flask_restful import Api
from flask_jwt import JWT
import psycopg2
from auth import authenticate, identity
from restaurantressource import createrestaurant
from restaurantressource import restaurantsList
from restaurantressource import getrestaurant
from restaurantressource import delrestaurant
from restaurantressource import putrestaurant
from restaurantressource import openrestaurants
from restaurantressource import closerestaurants
from userressource import UserRegister
from userressource import usersList


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'hawwaha'
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(createrestaurant, '/createrestaurant')
api.add_resource(restaurantsList, '/restaurants')
api.add_resource(getrestaurant, '/getrestaurant/<string:name>')
api.add_resource(delrestaurant, '/delrestaurant/<string:name>')
api.add_resource(putrestaurant, '/putrestaurant/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(usersList, '/users')
api.add_resource(openrestaurants, '/openrestaurants/<string:location>')
api.add_resource(closerestaurants, '/closerestaurants')



if __name__ == '__main__':
    app.run(debug=True)