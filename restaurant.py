import sqlite3

import psycopg2



class restaurantModel(object):
    def __init__(self, id, name, location, openingtime, closingtime):
        self.id = id
        self.name = name
        self.location = location
        self.openingtime=openingtime
        self.closingtime=closingtime
        
    @classmethod
    def find_by_name(cls, name):
        connection=psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()
        query="SELECT * FROM restaurants WHERE name=%s"
        result=cursor.execute(query, [name])
        row=cursor.fetchone()
        if row:
            restaurant=cls(*row)
        else:
            restaurant=None
        
        connection.close()
        return restaurant
    
    @classmethod
    def find_by_id(cls, id):
        connection=psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()

        query="SELECT * FROM restaurants WHERE id=%s"
        result=cursor.execute(query, [id])
        row=cursor.fetchone()
        if row:
            restaurant=cls(*row)
        else:
            restaurant=None
        
        connection.close()
        return restaurant
    
    def insert(self):
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()
        query="INSERT INTO restaurants(id,name,location,openingtime,closingtime) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query, (self.id, self.name, self.location, self.openingtime, self.closingtime))
        connection.commit()
        connection.close()


    def update(self):
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()
        query="UPDATE restaurants SET name=%s , location=%s , openingtime=%s , closingtime=%s WHERE id=%s"
        cursor.execute(query, (self.name, self.location, self.openingtime, self.closingtime, self.id))
        connection.commit()
        connection.close()
    
    def json(self) :
        return {'id':self.id, 'name':self.name, 'location': self.location, 'openingtime':self.openingtime, 'closingtime':self.closingtime}



'''
@classmethod
    def find_by_id(cls, id):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * FROM restaurants WHERE id=?"
        result=cursor.execute(query, (id,))
        row=result.fetchone()
        if row:
            restaurant=cls(*row)
        else:
            restaurant=None
        
        connection.close()
        return restaurant
    
    def insert(self):
        connection = psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()
        query="INSERT INTO restaurants VALUES(?,?,?,?,?)"
        cursor.execute(query, (self.id, self.name, self.location, self.openingtime, self.closingtime))
        connection.commit()
        connection.close()


    def update(self):
        connection = sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="UPDATE restaurants SET name=? AND location=? AND openingtime=? AND closingtime=? WHERE id=?"
        cursor.execute(query, (self.name, self.location, self.openingtime, self.closingtime, self.id))
        connection.commit()
        connection.close()
    
    def json(self) :
        return {'id':self.id, 'name':self.name, 'location': self.location, 'openingtime':self.openingtime, 'closingtime':self.closingtime}
'''