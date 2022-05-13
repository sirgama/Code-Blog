from flask  import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "login"

@auth.route("/sign_up")
def sign_up():
    return "sign_up"

@auth.route("/logout")
def logout():
    return "logout"