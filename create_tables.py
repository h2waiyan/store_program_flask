import sqlite3

connection = sqlite3.connect('mydatabase.db')

cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_user_table)

create_items_table = "CREATE TABLE IF NOT EXISTS items (name text, price text)"
cursor.execute(create_items_table)

test_data = "INSERT INTO items VALUES('test', 10.99)"
cursor.execute(test_data)

connection.commit()

connection.close()