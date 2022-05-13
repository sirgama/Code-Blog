from crypt import methods
from flask  import Blueprint, render_template, redirect, request, url_for

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return render_template('login.html')

@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    password = request.form.get('password1')
    return render_template('signup.html')

@auth.route("/logout")
def logout():
    return redirect(url_for('views.home'))