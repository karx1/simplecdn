from auth import AuthManager


class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.authenticated = False

    def make(self, username):
        with AuthManager() as auth:
            try:
                password = auth.get(username)
            except KeyError:
                return None
            else:
                self.username = username
                self.password = password
                return self

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
