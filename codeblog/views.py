from flask  import abort, render_template, redirect, url_for, flash, request
from codeblog import app, db, mail
from codeblog.models import User, Blog, Comment, Like, Dislike
from codeblog.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateForm,CommentForm
from flask_login import login_required, logout_user, login_user, current_user
from flask_mail import Message



@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
      
        
    return render_template('login.html')
    

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}!", 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html', form=form)

@app.route("/logout")
@login_required
def logout():
   
    return redirect(url_for('home'))
