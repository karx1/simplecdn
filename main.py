from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
from flask_login import LoginManager, login_user
from .user import User
from .auth import AuthManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
key_file = "data/system/key.txt"
if os.path.exists(key_file) and os.path.isfile(key_file):
    with open(key_file, "rb") as f:
        key = f.read()
else:
    key = os.urandom(16)
    os.makedirs(os.path.dirname(key_file), exist_ok=True)
    with open(key_file, "wb+") as f:
        f.write(key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all")
def all_files():
    files = os.listdir("data")
    return render_template("all.html", files=files)


@app.route("/upload", methods=["POST"])
def upload():
    if not request.method == "POST":
        return "Not using POST request. Maybe something went wrong?"
    file = request.files["file"]
    if file.filename == '':
        return "fatal: no selected file"
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join("data", filename))
        return redirect(url_for('send', filename=filename))


@app.route("/file/<filename>")
def send(filename):
    return send_from_directory("data", filename)


@login_manager.user_loader
def load_user(user_id):
    return User().make(user_id)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        user = User().make(username)
        with AuthManager() as auth:
            if auth.check_password(password, user.password):
                user.password = password
                user.authenticated = True
                login_user(user, remember=True)
                return redirect(url_for("home"))

    return render_template("login.html")


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
