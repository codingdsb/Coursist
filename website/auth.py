from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    # check if all fields are provided
    if (email == "") or (password == ""):
        flash("Please provide all the credentials")
        return redirect(url_for("auth.login"))

    # check if user exists
    user = User.query.filter_by(email=email).first()

    # if user not in db or if user's password not matching then throw error
    if not user or not check_password_hash(user.password, password):
        flash("Invalid credentials")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)

    return redirect(url_for("main.index"))



@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    # check if all fields are provided
    if (name == "") or (email == "") or (password == ""):
        flash("All fields (name, email and password) are required")
        return redirect(url_for("auth.signup"))
    # Check if user already exists with the provided email
    user = User.query.filter_by(email=email).first()
    if user:
        flash(f"The email ({email}) is already taken. If that's yours, then login else use another email address.")
        return redirect(url_for("auth.signup"))

    # Else create a new User object
    hashed_password = generate_password_hash(password, method="sha256")
    new_user = User(email=email, name=name, password=hashed_password)

    # And save it to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))