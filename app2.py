from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB
import os



# FLASK APP

app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)

# Secret key za session
app.secret_key = "123"



# BAZE

posts_db = TinyDB("db/posts.json")
users_db = TinyDB("db/users2.json")



# FOLDER ZA SLIKE

UPLOAD_FOLDER = "static2/uploads"



# GLAVNA STRAN

@app.route("/")
def index():

    # Če uporabnik ni prijavljen
    if "user" not in session:
        return redirect("/login")

    # Dobimo vse poste
    posts = posts_db.all()

    # Prikažemo index.html
    return render_template("index.html", posts=posts)



# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    # Če uporabnik pošlje formo
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Dobimo vse uporabnike
        users = users_db.all()

        # Preverimo uporabnike
        for user in users:

            # Če se username in password ujemata
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
    session.pop("user")

    return redirect("/login")



# DODAJANJE POSTA

@app.route("/add_post", methods=["POST"])
def add_post():

    # Dobimo text
    text = request.form["text"]

    # Dobimo sliko
    image = request.files["image"]

    # Default filename
    filename = ""

    # Če slika obstaja
    if image and image.filename != "":

        filename = image.filename

        # Shranimo sliko
        image.save(
            os.path.join(UPLOAD_FOLDER, filename)
        )

    # Dodamo post v bazo
    posts_db.insert({
        "user": session["user"],
        "text": text,
        "image": filename,
        "likes": 0
    })

    return jsonify({
        "status": "ok"
    })


# BRISANJE POSTA

@app.route("/delete_post", methods=["POST"])
def delete_post():

    # Dobimo ID posta
    post_id = int(request.form["id"])

    # Izbrišemo post
    posts_db.remove(doc_ids=[post_id])

    return jsonify({
        "status": "ok"
    })


# LIKE POSTA

@app.route("/like_post", methods=["POST"])
def like_post():

    # Dobimo ID posta
    post_id = int(request.form["id"])

    # Dobimo post
    post = posts_db.get(doc_id=post_id)

    # Povečamo likes
    new_likes = post.get("likes", 0) + 1

    # Update likes
    posts_db.update({
        "likes": new_likes
    }, doc_ids=[post_id])

    # Vrne novo število likeov
    return jsonify({
        "likes": new_likes
    })



# ZAGON APLIKACIJE

app.run(debug=True, port=5001)