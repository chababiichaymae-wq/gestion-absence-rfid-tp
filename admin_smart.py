from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "smarttp_secret"

def get_db():
    return sqlite3.connect("smarttp.db")

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM admins WHERE username=? AND password=?",
                    (username,password))
        admin = cur.fetchone()
        db.close()

        if admin:
            session["admin"] = username
            return redirect("/dashboard")
        else:
            return "Login incorrect ❌"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/login")
    return render_template("interface.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
