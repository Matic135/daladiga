from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB



# FLASK APP

app = Flask(
    __name__,
    template_folder="templates3",
    static_folder="static3"
)

# Secret key za session
app.secret_key = "123"



# BAZE

users_db = TinyDB("db2/users.json")
items_db = TinyDB("db2/items.json")



# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    # Če uporabnik pošlje formo
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Gremo čez vse uporabnike
        for user in users_db.all():

            # Preverimo username in password
            if user["username"] == username and user["password"] == password:

                # Shranimo uporabnika v session
                session["user"] = username

                return redirect("/")

    # Če je GET request
    return render_template("login.html")



# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():

    # Če uporabnik pošlje register formo
    if request.method == "POST":

        # Dodamo uporabnika v bazo
        users_db.insert({
            "username": request.form["username"],
            "password": request.form["password"]
        })

        return redirect("/login")

    # Če je GET request
    return render_template("register.html")



# LOGOUT

@app.route("/logout")
def logout():

    # Odstranimo uporabnika iz session
    session.pop("user", None)

    return redirect("/login")



# GLAVNA STRAN

@app.route("/")
def index():

    # Če uporabnik ni prijavljen
    if "user" not in session:
        return redirect("/login")

    # Dobimo vse iteme
    items = items_db.all()

    # Prikažemo index.html
    return render_template("index.html", items=items)



# DODAJ ITEM

@app.route("/add_item", methods=["POST"])
def add_item():

    # Dobimo ime itema
    name = request.form["name"]

    # Dodamo item v bazo
    item_id = items_db.insert({
        "user": session["user"],
        "name": name,
        "done": False
    })

    # Vrne podatke itema
    return jsonify({
        "id": item_id,
        "name": name
    })



# OZNAČI ITEM KOT DONE

@app.route("/done_item", methods=["POST"])
def done_item():

    # Dobimo ID itema
    item_id = int(request.form["id"])

    # Update done status
    items_db.update({
        "done": True
    }, doc_ids=[item_id])

    return jsonify({
        "status": "ok"
    })



# DELETE ITEM

@app.route("/delete_item", methods=["POST"])
def delete_item():

    # Dobimo ID itema
    item_id = int(request.form["id"])

    # Izbrišemo item
    items_db.remove(doc_ids=[item_id])

    return jsonify({
        "status": "ok"
    })



# ZAGON APLIKACIJE

app.run(debug=True, port=5003)