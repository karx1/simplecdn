import pickle
from passlib.context import CryptContext


class AuthManager:
    def __init__(self):
        self.filename = "data/auth.txt"
        self.auth = {}
        self.ctx = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
        )

    def __enter__(self):
        try:
            with open(self.filename, "rb") as file:
                d = pickle.load(file)
                for key, value in d.items():
                    self.auth[key] = value
        except (FileNotFoundError, EOFError):
            self.cache = {}
        finally:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.filename, "wb+") as file:
            d = {}
            for key, value in self.auth.items():
                d[key] = value
            pickle.dump(d, file)

    def keys(self):
        return self.auth.keys()

    def encrypt(self, password):
        return self.ctx.hash(password)

    def check_password(self, hashed, password):
        return self.ctx.verify(password, hashed)

    def add(self, username, password):
        assert username not in self.auth
        password = self.encrypt(password)
        self.auth[username] = password

    def get(self, username):
        return self.auth[username]
