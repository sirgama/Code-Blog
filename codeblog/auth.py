
from flask  import Blueprint, render_template, redirect, request, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return render_template('login.html')

@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email AlreadyIn Use', category='danger')
            
        elif username_exists:
            flash('username already exists', category='danger')
            
        elif password != password1:
            flash('Passwords dont match', category='danger')
            
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.commit(new_user)
            db.session.commit()
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))
            
        
    return render_template('signup.html')

@auth.route("/logout")
def logout():
    return redirect(url_for('views.home'))