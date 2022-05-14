from flask  import abort, render_template, redirect, url_for, flash, request
from codeblog import app, db, mail
from codeblog.models import User
from flask_login import login_required, logout_user, login_user



@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
      
        
    return render_template('login.html')
    

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    
        
    return render_template('signup.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
