from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates1")
app.secret_key = "123"

notes_db = TinyDB("db/notes.json")
users_db = TinyDB("db/users.json")


# -----------------------
# HOME
# -----------------------
@app.route("/")
def index():

    if "user" not in session:
        return redirect("/login")

    notes = notes_db.all()
    return render_template("index.html", notes=notes)


# -----------------------
# LOGIN
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        for u in users_db.all():
            if u["username"] == username and u["password"] == password:

                session["user"] = username
                return redirect("/")

        return redirect("/login")

    return render_template("login.html")


# -----------------------
# REGISTER
# -----------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        users_db.insert({
            "username": request.form["username"],
            "password": request.form["password"]
        })

        return redirect("/login")

    return render_template("register.html")


# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/login")


# -----------------------
# ADD NOTE
# -----------------------
@app.route("/add", methods=["POST"])
def add():

    notes_db.insert({
        "title": request.form["title"],
        "content": request.form["content"]
    })

    return redirect("/")


# -----------------------
# DELETE NOTE
# -----------------------
@app.route("/delete/<int:id>")
def delete(id):

    notes_db.remove(doc_ids=[id])
    return redirect("/")


# -----------------------
# RUN
# -----------------------
app.run(debug=True)