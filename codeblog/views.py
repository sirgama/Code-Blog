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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user, remember=form.remember.data)
            flash("Successful Login", 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Check Email or Password', 'danger')
            
        
    return render_template('login.html', form=form)
    

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
    logout_user()
    return redirect(url_for('home'))
