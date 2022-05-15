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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='minutepitcher@gmail.com', recipients=[user.email])
    
    msg.body = f''' To Reset Your Password,visit the following link:
    
    { url_for('reset_token', token=token, _external=True) } 
    
    If you did not make this request, ignore this mail and no changes will be made
    
    '''
    mail.send(msg)
    
    

@app.route("/reset_password", methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instructions on how to reset your password. Check Your Spam as well!', 'info')
    
    return render_template('reset_request.html', title='Request Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('Expired or invalid Token!', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        db.session.commit(password)
        flash('Password Reset Successfully, You can now login to access account features!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_token.html', title='Request Password', form=form)
