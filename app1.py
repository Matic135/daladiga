from flask import Flask, render_template, request, session, jsonify
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates1")
app.secret_key = "123"

notes_db = TinyDB("db/notes.json")
users_db = TinyDB("db/users.json")

@app.route("/")
def index():
    if "user" not in session:
        return render_template("login.html")
    notes = notes_db.all()
    return render_template("index.html", notes=notes)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for user in users_db:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                return jsonify({"status": "ok"})
        return jsonify({"status": "fail"})
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users_db.insert({
            "username": request.form["username"],
            "password": request.form["password"]
        })
        return jsonify({"status": "registered"})
    return render_template("register.html")
@app.route("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"status": "logged out"})


@app.route("/add", methods=["POST"])
def add():
    note = notes_db.insert({
        "title": request.form["title"],
        "content": request.form["content"]
    })
    return jsonify({
        "id": note,
        "title": request.form["title"],
        "content": request.form["content"]
    })

@app.route("/delete/<int:id>")
def delete(id):
    notes_db.remove(doc_ids=[id])
    return jsonify({"status": "deleted", "id": id})

app.run(debug=True)