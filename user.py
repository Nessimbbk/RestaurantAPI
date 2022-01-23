import sqlite3
import psycopg2



class UserModel(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection=psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()

        query="SELECT * FROM users WHERE username=%s"
        result=cursor.execute(query, [username])
        row=cursor.fetchone()
        if row:
            user=cls(*row)
        else:
            user=None
        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection=psycopg2.connect(user="postgres",
                        password="nessim",
                        host="localhost",
                        port="5432",
                        database="APIDB")
        cursor=connection.cursor()

        query="SELECT * FROM users WHERE id=%s"
        result=cursor.execute(query, [_id])
        row=cursor.fetchone()
        if row:
            user=cls(*row)
        else:
            user=None
        connection.close()
        return user