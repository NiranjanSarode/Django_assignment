import sqlite3
import requests
# print({{ request.user.username }})

conn = sqlite3.connect('db.sqlite3')

cursor = conn.cursor()

cursor.execute('SELECT * FROM home_sales')

tables = cursor.fetchall()


for table in tables:
    print(table)


cursor.close()
conn.close()
