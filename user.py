class User:
    def __init__(self, username, password, auth):
        self.username = username
        self.password = password
        self.authenticated = auth

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
