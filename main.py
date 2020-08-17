from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from user import User
from auth import AuthManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
key_file = "data/key.txt"
if os.path.exists(key_file) and os.path.isfile(key_file):
    with open(key_file, "rb") as f:
        key = f.read()
else:
    key = os.urandom(16)
    os.makedirs(os.path.dirname(key_file), exist_ok=True)
    with open(key_file, "wb+") as f:
        f.write(key)

app.secret_key = key


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/all")
def all_files():
    files = []
    for level in os.listdir("data"):
        print(level)
        if os.path.isdir(f"data/{level}"):
            print("Is directory")
            for file in os.listdir(f"data/{level}"):
                files.append(f"{level}/{file}")
    print(files)
    return render_template("all.html", files=files)


@app.route("/upload", methods=["POST"])
def upload():
    user = current_user
    name = user.get_id()
    if not request.method == "POST":
        return "Not using POST request. Maybe something went wrong?"
    file = request.files["file"]
    if file.filename == '':
        return "fatal: no selected file"
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join("data", name), filename))
        return redirect(url_for('send', user=name, filename=filename))


@app.route("/file/<user>/<filename>")
def send(user, filename):
    filename = secure_filename(filename)
    return send_from_directory("data", os.path.join(user, filename))


@login_manager.user_loader
def load_user(user_id):
    with AuthManager() as auth:
        hashed = auth.get(user_id)
        return User(user_id, hashed, False)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        with AuthManager() as auth:
            hashed = auth.get(username)
            if auth.check_password(hashed, password):
                user = User(username, password, True)
                login_user(user, remember=True)
                return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        with AuthManager() as auth:
            auth.add(username, password)
            os.makedirs(os.path.join("data", username), exist_ok=False)
            return redirect(url_for("login_page"))

    return render_template("signup.html")


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login_page"))


@app.route("/logout")
@login_required
def logout():
    user = current_user
    name = user.get_id()
    logout_user()
    return f"Goodbye, {name}!"


@app.route("/profile")
@login_required
def profile():
    user = current_user
    files = os.listdir(f"data/{user.get_id()}")
    return render_template("profile.html", user=user, files=files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
