import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from database import init_db, add_user, verify_user, add_ioc, get_recent, find_ioc
import sqlite3

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
bcrypt = Bcrypt(app)


# Initialize DB
init_db()

# --------------------------
# AUTH ROUTES
# --------------------------

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    
    role = session["user"]["role"]
    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    else:
        return redirect(url_for("user_dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = verify_user(username, password)
        if user:
            session["user"] = user
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form.get("role", "user")
        try:
            add_user(username, password, role)
            return redirect(url_for("login"))
        except Exception as e:
            return render_template("register.html", error=str(e))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --------------------------
# ADMIN DASHBOARD
# --------------------------

@app.route("/admin")
def admin_dashboard():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("login"))
    iocs = get_recent(50)
    return render_template("admin.html", iocs=iocs, user=session["user"])


@app.route("/add_ioc", methods=["POST"])
def add_ioc_route():
    if "user" not in session or session["user"]["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    url = request.form.get("url")
    if url:
        add_ioc(url, "manual")
        return redirect(url_for("admin_dashboard"))
    return jsonify({"error": "No URL provided"}), 400

# --------------------------
# USER DASHBOARD
# --------------------------

@app.route("/user")
def user_dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    iocs = get_recent(50)
    return render_template("user.html", iocs=iocs, user=session["user"])

# --------------------------
# SEARCH
# --------------------------

@app.route("/search", methods=["POST"])
def search():
    url = request.form.get("url")
    result = find_ioc(url)
    return render_template("search.html", result=result, user=session.get("user"))

# --------------------------

if __name__ == "__main__":
    app.run(debug=True)
