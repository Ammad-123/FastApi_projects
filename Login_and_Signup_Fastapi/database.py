fake_users_db = {}



def get_user(username: str):
    return fake_users_db.get(username)
