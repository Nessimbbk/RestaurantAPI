import sqlite3
from flask_restful import Resource, reqparse
from user import UserModel
from flask_jwt import jwt_required
import psycopg2

        
class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required= True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required= True, help="This field cannot be left blank!")
    
    def post(self):
        data=UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return{"message": "User with that username already exists."}, 400
        
        connection=psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor = connection.cursor()
        
        query= "INSERT INTO users VALUES (default, %s, %s)"
        cursor.execute(query, (data['username'], data['password'])) 
        connection.commit()
        connection.close()
        
        return{"message": "User created successfully."}, 201
    
class usersList(Resource):
    @jwt_required()
    def get(self):
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()
        query="SELECT * FROM users"
        result = cursor.execute(query)
        users = []
        for row in cursor:
            users.append({'id': row[0], 'username': row[1], 'password': row[2]})
        connection.close()
        
        return {'Users': users}