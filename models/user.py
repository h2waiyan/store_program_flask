import sqlite3

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username): 
        connection = sqlite3.connect('mydatabase.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users where username=?"
        result = cursor.execute(query, (username, ))
        row = result.fetchone()
        print(row)
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None 

        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, _id):
        connection = sqlite3.connect('mydatabase.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users where id=?"
        result = cursor.execute(query, (_id, ))
        row = result.fetchone()
        print(row)
        if row:
            user = cls(*row)
        else:
            user = None 

        connection.close()
        return user