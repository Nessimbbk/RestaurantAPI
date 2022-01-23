import sqlite3
import psycopg2
from flask_restful import Resource, reqparse


def __init__(self, id, name, location, openingtime, closingtime):
        self.id = id
        self.name = name
        self.location = location
        self.openingtime=openingtime
        self.closingtime=closingtime
@classmethod
def find_by_name(cls, name):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * FROM restaurants WHERE name=?"
        result=cursor.execute(query, (name,))
        row=result.fetchone()
        if row:
            restaurant=cls(*row)
        else:
            restaurant=None
        
        connection.close()
        return restaurant
def update(self):
        connection = sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="UPDATE restaurants SET name=? AND location=? AND openingtime=? AND closingtime=? WHERE id=?"
        cursor.execute(query, (self.name, self.location, self.openingtime, self.closingtime, self.id))
        connection.commit()
        connection.close()
    
def json(self) :
        return {'id':self.id, 'name':self.name, 'location': self.location, 'openingtime':self.openingtime, 'closingtime':self.closingtime}


parser = reqparse.RequestParser()
parser.add_argument('id', type=int, required=True,
                        help="This field cannot be left blank!")
parser.add_argument('location', type=str, required=True,
                        help="This field cannot be left blank!")
parser.add_argument('openingtime', type=str, required=True,
                        help="This field cannot be left blank!")
parser.add_argument('closingtime', type=str, required=True,
                        help="This field cannot be left blank!")

def put(self, name):
        data = parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = find_by_name(name)
        updated_item = (data['id'], name, data['location'], data['openingtime'], data['closingtime'])

        if item is None:
            try:
                updated_item.insert()
            except:
                # internal server error
                return{"message": "An error occured when inserting the item"}, 500
        else:
            try:
                updated_item.update()
            except:
                # internal server error
                return{"message": "An error occured when updating the item"}, 500
        return updated_item.json()

print(put(self=True,name="kfc"))



"""
conn = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")

cursor = conn.cursor()
query="SELECT * FROM restaurants where location=%s"
result=cursor.execute(query, ["monastir"])
row=cursor.fetchall()
if row:
    restaurant=row
else:
    restaurant=None
print ("result:"+str(restaurant))
"""
'''
GET CURRENT TIME
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
'''
'''
cursor = conn.cursor()
name =input ("Enter name :")
gettable="SELECT * FROM restaurants"
result=cursor.execute(gettable, (name,))
row=result.fetchall()'''