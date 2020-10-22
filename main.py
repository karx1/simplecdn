from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_from_directory,
    url_for,
    flash,
)
from werkzeug.utils import secure_filename
import os
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from user import User
from auth import AuthManager
from env import check_env, check_env_bool

app = Flask(__name__)

if app.testing:
    DATA_DIR = "data"
else:
    # Not in testing mode, check whether we are running on docker
    DATA_DIR = check_env()

login_manager = LoginManager()
login_manager.init_app(app)
key_file = f"{DATA_DIR}/key.txt"
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
    for level in os.listdir(DATA_DIR):
        print(level)
        if os.path.isdir(f"{DATA_DIR}/{level}"):
            print("Is directory")
            for file in os.listdir(f"{DATA_DIR}/{level}"):
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
    if file.filename == "":
        flash("No file was provided!")
        return redirect(url_for("home"))
    if file:
        filename = os.path.join(os.path.join(DATA_DIR, name), secure_filename(file.filename))
        if os.path.isfile(filename):
            flash("This file already exists!")
            return redirect(url_for("home"))
        file.save(filename)
        return redirect(url_for("send", user=name, filename=filename))


@app.route("/file/<user>/<filename>")
def send(user, filename):
    filename = secure_filename(filename)
    return send_from_directory(DATA_DIR, os.path.join(user, filename))


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
        if username == "":
            flash("No username was provided.")
            return redirect(url_for("login_page"))
        elif password == "":
            flash("No password was provided")
            return redirect(url_for("login_page"))
        with AuthManager() as auth:
            try:
                hashed = auth.get(username)
            except KeyError:
                flash("Your username or password was incorrect.")
                return redirect(url_for("login_page"))
            if auth.check_password(hashed, password):
                user = User(username, password, True)
                login_user(user, remember=True)
                return redirect(url_for("home"))
            else:
                flash("Your username or password was incorrect.")
                return redirect(url_for("login_page"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        if username == "":
            flash("No username was provided")
            return redirect(url_for("register"))
        elif password == "":
            flash("No password was provided")
            return redirect(url_for("register"))
        with AuthManager() as auth:
            try:
                auth.add(username, password)
            except AssertionError:
                flash("This username is already taken.")
                return redirect(url_for("register"))
            os.makedirs(os.path.join(DATA_DIR, username), exist_ok=True)
            flash("Successfully registered. Please login below.")
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
    flash(f"Goodbye, {name}!")
    return redirect(url_for("login_page"))


@app.route("/profile")
@login_required
def profile():
    user = current_user
    files = os.listdir(f"{DATA_DIR}/{user.get_id()}")
    return render_template("profile.html", user=user, files=files)

@app.route("/user")
@login_required
def user():
    return {
        "username": current_user.get_id(),
        "password": current_user.password
    }


if __name__ == "__main__":
    if check_env_bool():
        port = 8080
        debug = False
    else:
        port = 7080
        debug = True
    if app.testing:
        port = 7080
        debug = True
    app.run(host="0.0.0.0", port=port, debug=debug)
