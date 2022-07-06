from models.user import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username) #getting the username from the dictionary .get is another way of ['username']
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)

