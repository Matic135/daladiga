from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates3", static_folder="static3")
app.secret_key = "123"

users_db = TinyDB("db2/users.json")
items_db = TinyDB("db2/items.json")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for u in users_db:
            if u["username"] == username and u["password"] == password:
                session["user"] = username
                return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        users_db.insert({
            "username": request.form["username"],
            "password": request.form["password"]
        })
        return redirect("/login")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    items = items_db.all()
    return render_template("index.html", items=items)


@app.route("/add_item", methods=["POST"])
def add_item():

    name = request.form["name"]
    item_id = items_db.insert({
        "user": session["user"],
        "name": name,
        "done": False
    })

    return jsonify({
        "id": item_id,
        "name": name
    })


@app.route("/done_item", methods=["POST"])
def done_item():

    item_id = int(request.form["id"])
    items_db.update({"done": True}, doc_ids=[item_id])
    return jsonify({"status":"ok"})


@app.route("/delete_item", methods=["POST"])
def delete_item():
    item_id = int(request.form["id"])
    items_db.remove(doc_ids=[item_id])
    return jsonify({"status":"ok"})

app.run(debug=True, port=5003)