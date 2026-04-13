from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB
import os

app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = "123"

posts_db = TinyDB("db/posts.json")
users_db = TinyDB("db/users2.json")

UPLOAD_FOLDER = "static2/uploads"


@app.route("/")
def index():

    if "user" not in session:
        return redirect("/login")

    posts = posts_db.all()
    return render_template("index.html", posts=posts)


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = users_db.all()

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users_db.insert({
            "username": username,
            "password": password
        })

        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():

    session.pop("user")
    return redirect("/login")


@app.route("/add_post", methods=["POST"])
def add_post():

    text = request.form["text"]
    image = request.files["image"]

    filename = ""

    if image:
        filename = image.filename
        image.save(os.path.join(UPLOAD_FOLDER, filename))

    posts_db.insert({
        "user": session["user"],
        "text": text,
        "image": filename
    })

    return redirect("/")


app.run(debug=True, port=5001)