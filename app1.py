from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB

# Ustvarimo Flask aplikacijo
app = Flask(
    __name__,
    template_folder="templates1"
)

# Secret key za session
app.secret_key = "123"

# Povezava na TinyDB bazi
notes_db = TinyDB("db/notes.json")
users_db = TinyDB("db/users.json")



# HOME

@app.route("/")
def index():

    # Če uporabnik ni prijavljen, ga preusmerimo na login
    if "user" not in session:
        return redirect("/login")

    # Preberemo vse zapiske iz baze
    all_notes = notes_db.all()

    notes = []

    # Vsakemu zapisku dodamo doc_id
    for note in all_notes:
        note["doc_id"] = note.doc_id
        notes.append(note)

    # Pošljemo podatke v index.html
    return render_template(
        "index.html",
        notes=notes,
        username=session["user"]
    )



# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    # Če uporabnik pošlje login formo
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Preberemo vse uporabnike
        users = users_db.all()

        # Poiščemo ujemanje username + password
        for user in users:

            if (
                user["username"] == username
                and user["password"] == password
            ):

                # Shranimo uporabnika v session
                session["user"] = username

                return redirect("/")

        # Če prijava ni uspešna
        return redirect("/login")

    # Prikažemo login stran
    return render_template("login.html")



# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():

    # Če uporabnik pošlje register formo
    if request.method == "POST":

        # Dodamo novega uporabnika v bazo
        users_db.insert({
            "username": request.form["username"],
            "password": request.form["password"]
        })

        return redirect("/login")

    # Prikažemo register stran
    return render_template("register.html")



# LOGOUT

@app.route("/logout")
def logout():

    # Izbrišemo uporabnika iz session
    session.pop("user", None)

    return redirect("/login")



# ADD NOTE (AJAX)

@app.route("/add_note", methods=["POST"])
def add_note():

    # Preverimo ali je uporabnik prijavljen
    if "user" not in session:
        return jsonify({"success": False})

    # Preberemo JSON podatke iz fetch zahteve
    data = request.get_json()

    # Shranimo nov zapisek v bazo
    notes_db.insert({
        "title": data["title"],
        "content": data["content"],
        "owner": session["user"]
    })

    # Vrnemo odgovor JavaScriptu
    return jsonify({"success": True})



# DELETE NOTE (AJAX)

@app.route("/delete_note/<int:id>", methods=["POST"])
def delete_note(id):

    # Izbrišemo zapisek po doc_id
    notes_db.remove(doc_ids=[id])

    # Vrnemo uspešen odgovor
    return jsonify({"success": True})



# EDIT NOTE (AJAX)

@app.route("/edit_note/<int:id>", methods=["POST"])
def edit_note(id):

    # Preberemo nove podatke iz JSON-a
    data = request.get_json()

    # Posodobimo naslov in vsebino
    notes_db.update(
        {
            "title": data["title"],
            "content": data["content"]
        },
        doc_ids=[id]
    )

    # Vrnemo uspešen odgovor
    return jsonify({"success": True})



# RUN

if __name__ == "__main__":

    # Zaženemo Flask strežnik
    app.run(debug=True, port=5000)