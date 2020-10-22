from unittest import TestCase, defaultTestLoader
from main import app
from auth import AuthManager
from io import BytesIO


def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare


ordered, compare = make_orderer()
defaultTestLoader.sortTestMethodsUsing = compare


class SimpleCDNTests(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self._ctx = app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        if self._ctx:
            self._ctx.pop()

    @ordered
    def test_user_registration(self):
        with self.client:
            self.client.post("register", data={"email": "test", "password": "testpass"})

            with AuthManager() as auth:
                self.assertIn("test", auth.keys())

    @ordered
    def test_login(self):
        with self.client:
            self.client.post("login", data={"email": "test", "password": "testpass"})

            current_user = self.client.get("user").get_json()

            self.assertEqual(current_user["username"], "test")

    @ordered
    def test_upload(self):
        with self.client:
            self.client.post("login", data={"email": "test", "password": "testpass"})

            response = self.client.post(
                "upload", data={"file": (BytesIO(b"Test file"), "test.txt")}
            )

            self.assertEqual(response.status_code, 302)

    @ordered
    def test_get_file(self):
        with self.client:
            response = self.client.get("/file/test/test.txt")
            text = response.data.decode("UTF-8")

            self.assertEqual(text, "Test file")
