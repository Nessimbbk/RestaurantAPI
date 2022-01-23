import sqlite3

connection=sqlite3.connect('data.db')
cursor=connection.cursor()

create_table="CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

cursor.execute("INSERT INTO users VALUES (1,'nessim','boubaker')")


create_table="CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY, name text, location text, openingtime str, closingtime str)"
cursor.execute(create_table)


cursor.execute("INSERT INTO restaurants VALUES (1,	'kfc',	'monastir',	'08:00:00',	'00:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (2,	'burger king',	'tunis',	'06:30:00',	'22:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (3,	'mcdonalds',	'tunis',	'16:00:00',	'02:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (4,	'golden',	'monastir',	'00:00:00',	'00:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (5,	'bacha',	'monastir',	'18:00:00',	'04:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (6,	'silver',	'sousse',	'10:00:00',	'21:00:00')")
cursor.execute("INSERT INTO restaurants VALUES (7,	'aromate',	'monastir',	'09:00:00',	'01:00:00')")
''''
1	"kfc"	"Monastir"	"08:00:00"	"00:00:00"
2	"burger king"	"tunis"	"06:30:00"	"22:00:00"
3	"mcdonalds"	"tunis"	"16:00:00"	"02:00:00"
4	"golden"	"monastir"	"00:00:00"	"00:00:00"
5	"bacha"	"monastir"	"18:00:00"	"04:00:00"
6	"silver"	"monastir"	"10:00:00"	"21:00:00"
7	"aromate"	"sousse"	"09:00:00"	"01:00:00"
8	"viking"	"monastir"	"00:00:00"	"00:00:00"
'''
connection.commit()
connection.close()