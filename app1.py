from flask import Flask, render_template, request, redirect, session, url_for
from tinydb import TinyDB, Query

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = "tajna_koda"  # za session

db = TinyDB("db/notes.json")
Note = Query()

# Minimalni uporabniki za demo
users = {
    "dijak": "geslo123",
    "test": "test123"
}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Napačno uporabniško ime ali geslo")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    notes = db.all()
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    if "user" not in session:
        return redirect(url_for("login"))
    title = request.form.get("title")
    content = request.form.get("content")
    db.insert({"title": title, "content": content})
    return redirect(url_for("index"))


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    if "user" not in session:
        return "Nedovoljen dostop", 403
    db.remove(doc_ids=[note_id])
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, port=5000)