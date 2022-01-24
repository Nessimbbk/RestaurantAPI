from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import psycopg2
import geocoder
from geopy.geocoders import Nominatim
from datetime import datetime
from restaurant import restaurantModel
from restaurant import restaurantModel


class createrestaurant(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('location', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('openingtime', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('closingtime', type=str, required=True,
                        help="This field cannot be left blank!")

    @jwt_required()
    def post(self):
        data = createrestaurant.parser.parse_args()

        if restaurantModel.find_by_name(data['name'].lower()):
            return{"message": "restaurant with that name already exists."}, 400

        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor = connection.cursor()
        id1=data['id']
        name=data['name']
        location=data['location']
        open=data['openingtime']
        close=data['closingtime']
        query="INSERT INTO restaurants(id,name,location,openingtime,closingtime) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query, (id1,name.lower(),location,open,close))
        connection.commit()
        connection.close()

        return{"message": "Restaurant created successfully."}, 201


class restaurantsList(Resource):
    
    def get(self):
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor = connection.cursor()
        query = "SELECT * FROM restaurants order by id asc"
        cursor.execute(query)
        return {'Restaurants ': cursor.fetchall()}


class getrestaurant(Resource):
    def get(self, name):
        restaurant = restaurantModel.find_by_name(name.lower())
        if restaurant:
            return restaurant.json()
        return{'message': 'restaurant not found'}, 404


class delrestaurant(Resource):
    @jwt_required()
    def delete(self, name):
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor = connection.cursor()
        query = "DELETE FROM restaurants WHERE name=%s"
        cursor.execute(query, [name])
        restaurant = restaurantModel.find_by_name(name.lower())
        if restaurant:
            connection.commit()
            connection.close()
            return {'message': 'restaurant deleted'}
        return {'message': 'there is no restaurant with that name'}


class putrestaurant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('location', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('openingtime', type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('closingtime', type=str, required=True,
                        help="This field cannot be left blank!")

    @jwt_required()
    def put(self, name):
        data = putrestaurant.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = restaurantModel.find_by_name(name.lower())
        updated_item = restaurantModel(
            data['id'], name.lower(), data['location'], data['openingtime'], data['closingtime'])

        if item is None:
            try:
                updated_item.insert()
            except:
                # internal server error
                return{"message": "An error occured when inserting the restaurant"}, 500
        else:
            try:
                updated_item.update()
            except:
                # internal server error
                return{"message": "An error occured when updating the restaurant"}, 500
            
        return updated_item.json()


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

class openrestaurants(Resource):
    
    def get(self,location):
        now = datetime.now()
        currenttime = now.strftime("%H:%M:%S")
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor = connection.cursor()
        query = "SELECT * FROM restaurants"
        result = cursor.execute(query)
        restaurants = []
        for row in cursor:
            timeEnd = datetime.strptime(row[4], "%H:%M:%S")
            timeStart = datetime.strptime(row[3], "%H:%M:%S")
            timeNow = datetime.strptime(currenttime, "%H:%M:%S")
            check=isNowInTimePeriod(timeStart, timeEnd, timeNow)
            if check and row[2].lower()==location.lower():
                restaurants.append(
                    {'id': row[0], 'name': row[1], 'location': row[2], 'openingtime': row[3], 'closingtime': row[4]})
        connection.close()
        
        return {"Open restaurants right now in that area ": restaurants}

class closerestaurants(Resource):

    def get(self):
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor = connection.cursor()
        query = "SELECT * FROM restaurants"
        result = cursor.execute(query)
        restaurants = []
        for row in cursor:
            restaurants.append(
                {'id': row[0], 'name': row[1], 'location': row[2], 'openingtime': row[3], 'closingtime': row[4]})
        connection.close()
        g = geocoder.ip('me')
        l=g.latlng
        '''latitude=str(l[0])
        longitude=str(l[1])'''
        latitude=g.geojson['features'][0]['properties']['lat']
        longitude=g.geojson['features'][0]['properties']['lng']
        geolocator = Nominatim(user_agent="getlocation")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        return {'Location':str(location) }


'''
        timeStart = '18:33:00'
        timeEnd = '11:00:00'
        timeNow = now.strftime("%H:%M:%S")
        timeEnd = datetime.strptime(timeEnd, "%H:%M:%S")
        timeStart = datetime.strptime(timeStart, "%H:%M:%S")
        timeNow = datetime.strptime(timeNow, "%H:%M:%S")
        resultf=isNowInTimePeriod(timeStart, timeEnd, timeNow)
        return {"Current Time =": resultf}



def get(self):
        now = datetime.now()
        currenttime = now.strftime("%H:%M:%S")
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM restaurants"
        result = cursor.execute(query)
        restaurants = []
        for row in result:
            timeEnd = datetime.strptime(row[4], "%H:%M:%S")
            timeStart = datetime.strptime(row[3], "%H:%M:%S")
            timeNow = datetime.strptime(currenttime, "%H:%M:%S")
            check=isNowInTimePeriod(timeStart, timeEnd, timeNow)
            if check:
                restaurants.append(
                    {'id': row[0], 'name': row[1], 'location': row[2], 'openingtime': row[3], 'closingtime': row[4]})
        connection.close()
        
        return {"Current Time =": restaurants}



class restaurantsList(Resource):
    
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM restaurants"
        result = cursor.execute(query)
        restaurants = []
        for row in result:
            restaurants.append(
                {'id': row[0], 'name': row[1], 'location': row[2], 'openingtime': row[3], 'closingtime': row[4]})
        connection.close()

        return {'items': restaurants}

def post(self):
        data = createrestaurant.parser.parse_args()

        if restaurantModel.find_by_name(data['name']):
            return{"message": "restaurant with that name already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO restaurants VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (data['id'], data['name'],
                       data['location'], data['openingtime'], data['closingtime']))
        connection.commit()
        connection.close()

        return{"message": "User created successfully."}, 201
        
        
def delete(self, name):
        #global items
        #items = list(filter(lambda x: x['name'] != name, items))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM restaurants WHERE name=?"
        cursor.execute(query, (name,))
        restaurant = restaurantModel.find_by_name(name)
        if restaurant:
            connection.commit()
            connection.close()
            return {'message': 'restaurant deleted'}
        return {'message': 'there is no restaurant with that name'}

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

class openrestaurants(Resource):
    
    def get(self,location):
        now = datetime.now()
        currenttime = now.strftime("%H:%M:%S")
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM restaurants"
        result = cursor.execute(query)
        restaurants = []
        for row in result:
            timeEnd = datetime.strptime(row[4], "%H:%M:%S")
            timeStart = datetime.strptime(row[3], "%H:%M:%S")
            timeNow = datetime.strptime(currenttime, "%H:%M:%S")
            check=isNowInTimePeriod(timeStart, timeEnd, timeNow)
            if check and row[2].lower()==location.lower():
                restaurants.append(
                    {'id': row[0], 'name': row[1], 'location': row[2], 'openingtime': row[3], 'closingtime': row[4]})
        connection.close()
        
        return {"Current Time =": restaurants}

class closerestaurants(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM restaurants"
        result = cursor.execute(query)
        restaurants = []
        for row in result:
            restaurants.append(
                {'id': row[0], 'name': row[1], 'location': row[2], 'openingtime': row[3], 'closingtime': row[4]})
        connection.close()
        g = geocoder.ip('me')
        """print(g.latlng)"""
        l=g.latlng
        """latitude=str(l[0])
        longitude=str(l[1])"""
        latitude=g.geojson['features'][0]['properties']['lat']
        longitude=g.geojson['features'][0]['properties']['lng']
        geolocator = Nominatim(user_agent="getlocation")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        return {'items':str(location) }

        '''