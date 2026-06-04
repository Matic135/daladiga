from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB

app = Flask(
    __name__,
    template_folder="templates1"
)

app.secret_key = "123"

notes_db = TinyDB("db/notes.json")
users_db = TinyDB("db/users.json")



# HOME

@app.route("/")
def index():

    if "user" not in session:
        return redirect("/login")

    all_notes = notes_db.all()

    notes = []

    for note in all_notes:
        note["doc_id"] = note.doc_id
        notes.append(note)

    return render_template(
        "index.html",
        notes=notes,
        username=session["user"]
    )



# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = users_db.all()

        for user in users:

            if (
                user["username"] == username
                and user["password"] == password
            ):

                session["user"] = username
                return redirect("/")

        return redirect("/login")

    return render_template("login.html")



# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        users_db.insert({
            "username": request.form["username"],
            "password": request.form["password"]
        })

        return redirect("/login")

    return render_template("register.html")



# LOGOUT

@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/login")



# ADD NOTE (AJAX)

@app.route("/add_note", methods=["POST"])
def add_note():

    if "user" not in session:
        return jsonify({"success": False})

    data = request.get_json()

    notes_db.insert({
        "title": data["title"],
        "content": data["content"],
        "owner": session["user"]
    })

    return jsonify({"success": True})



# DELETE NOTE (AJAX)

@app.route("/delete_note/<int:id>", methods=["POST"])
def delete_note(id):

    notes_db.remove(doc_ids=[id])

    return jsonify({"success": True})


# EDIT NOTE (AJAX)

@app.route("/edit_note/<int:id>", methods=["POST"])
def edit_note(id):

    data = request.get_json()

    notes_db.update(
        {
            "title": data["title"],
            "content": data["content"]
        },
        doc_ids=[id]
    )

    return jsonify({"success": True})



# RUN

if __name__ == "__main__":
    app.run(debug=True, port=5000)