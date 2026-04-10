from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates1")
app.secret_key = "123"

notes_db = TinyDB("db/notes.json")
users_db = TinyDB("db/users.json")


@app.route("/")
def index():

    if "user" not in session:
        return redirect("/login")

    notes = notes_db.all()
    return render_template("index.html", notes=notes)


@app.route("/login", methods=["GET", "POST"])
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


@app.route("/register", methods=["GET", "POST"])
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


@app.route("/add", methods=["POST"])
def add():

    title = request.form["title"]
    content = request.form["content"]

    notes_db.insert({
        "title": title,
        "content": content
    })

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    notes_db.remove(doc_ids=[id])
    return redirect("/")


app.run(debug=True)