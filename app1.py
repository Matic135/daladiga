from flask import Flask, render_template, request, session, jsonify
from tinydb import TinyDB

# Ustvarimo Flask aplikacijo
app = Flask(__name__, template_folder="templates1")

# Secret key za session
app.secret_key = "123"

# Povezava na bazo
notes_db = TinyDB("db/notes.json")
users_db = TinyDB("db/users.json")



# GLAVNA STRAN

@app.route("/")
def index():

    # Če uporabnik ni prijavljen
    if "user" not in session:
        return render_template("login.html")

    # Dobimo vse zapiske
    notes = notes_db.all()

    # Prikažemo index.html
    return render_template("index.html", notes=notes)



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

                return jsonify({"status": "ok"})

        # Če login ni pravilen
        return jsonify({"status": "fail"})

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

        return jsonify({"status": "registered"})

    # Če je GET request
    return render_template("register.html")



# LOGOUT

@app.route("/logout")
def logout():

    # Odstranimo uporabnika iz session
    session.pop("user", None)

    return jsonify({"status": "logged out"})



# DODAJANJE ZAPISKA

@app.route("/add", methods=["POST"])
def add():

    # Dodamo nov zapisek
    note_id = notes_db.insert({
        "title": request.form["title"],
        "content": request.form["content"]
    })

    # Vrne podatke novega zapiska
    return jsonify({
        "id": note_id,
        "title": request.form["title"],
        "content": request.form["content"]
    })



# BRISANJE ZAPISKA

@app.route("/delete/<int:id>")
def delete(id):

    # Izbrišemo zapisek po ID-ju
    notes_db.remove(doc_ids=[id])

    return jsonify({
        "status": "deleted",
        "id": id
    })



# ZAGON APLIKACIJE

app.run(debug=True)