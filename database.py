
import psycopg2

connection = psycopg2.connect(user='postgres', password='nessim', host='localhost', port= '5432')
connection.autocommit = True
cursor = connection.cursor()
sql = "CREATE database APIDB"
cursor.execute(sql)
print("Database created successfully........")


connection = psycopg2.connect(database="APIDB",user='postgres', password='nessim', host='localhost', port= '5432')
connection.autocommit = True
cursor = connection.cursor()
create_table="CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY, name text, location text, openingtime Text, closingtime Text)"
cursor.execute(create_table)
print("Table restaurants Added")
cursor.execute("INSERT INTO restaurants VALUES (1,	'kfc',	'monastir',	'08:00:00',	'00:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (2,	'burger king',	'tunis',	'06:30:00',	'22:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (3,	'mcdonalds',	'tunis',	'16:00:00',	'02:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (4,	'golden',	'monastir',	'00:00:00',	'00:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (5,	'bacha',	'monastir',	'18:00:00',	'04:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (6,	'silver',	'sousse',	'10:00:00',	'21:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (7,	'aromate',	'monastir',	'09:00:00',	'01:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (8,	'viking',	'monastir',	'00:00:00',	'00:00:00')")
create_tableusers="CREATE TABLE IF NOT EXISTS users (id Serial NOT NULL PRIMARY KEY , username text, password text)"
cursor.execute(create_tableusers)
print("Table users Added")
cursor.execute("INSERT INTO users(id,username,password) VALUES (Default,'nessim','boubaker')")

connection.close()