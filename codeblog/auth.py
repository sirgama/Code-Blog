
from flask  import Blueprint, render_template, redirect, request, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user



auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        user =  User.query.filter_by(email=email).first()
        password = User.query.filter_by(password=password).first()
        if user and password:
            login_user(user, remember=True)
            flash('Successfully logged in', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect username password', category='danger')
    else:

        flash('User does not Exist', category='info')  
        
    return render_template('login.html')
    

@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email AlreadyIn Use', category='danger')
            
        elif username_exists:
            flash('username already exists', category='danger')
            
        elif password != password2:
            flash('Passwords dont match', category='danger')
            
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.commit(new_user)
            db.session.commit()
            
            flash('Account Created', category='success')
            return redirect(url_for('views.login'))
            
        
    return render_template('signup.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))