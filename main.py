from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all")
def all_files():
    files = os.listdir("files")
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
        file.save(os.path.join("files", filename))
        return redirect(url_for('send', filename=filename))


@app.route("/file/<filename>")
def send(filename):
    return send_from_directory("files", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
