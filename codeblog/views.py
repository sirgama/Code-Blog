import os
import secrets
from flask  import abort, render_template, redirect, url_for, flash, request
from codeblog import app, db, mail
from codeblog.models import User, Blog, Comment, Like, Dislike
from codeblog.forms import BlogForm, LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateForm,CommentForm
from flask_login import login_required, logout_user, login_user, current_user
from flask_mail import Message



@app.route('/home', methods=['GET', 'POST'])
def home():
    comments = Comment.query.all()
    blogs = Blog.query.all()
    user = User.query.all()
    users = list(reversed(user))
    limit = 20
    coding = Blog.query.filter_by(category = 'Coding').all()
    resources= Blog.query.filter_by(category = 'Resources').all()
    trends= Blog.query.filter_by(category = 'Trends').all()
    codenmoney = Blog.query.filter_by(category = 'Code & Money').all()
    
    return render_template('home.html', blogs = blogs,limit=limit, coding=coding, resources=resources, trends=trends, codenmoney=codenmoney, users=users, comments=comments)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html', title='Login', form=form)

    

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
    msg = Message('Password reset request', sender='minuteBloger@gmail.com', recipients=[user.email])
    
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
    
    return render_template('token_reset.html', title='Request Password', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/user_profiles', picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
    
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated Successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='user_profiles/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    
    if form.validate_on_submit():
        blog = Blog(title=form.title.data, category=form.category.data , content=form.content.data,  author=current_user )
        db.session.add(blog)
        db.session.commit()
        flash('Blog Created Successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_blog.html', title='New Blog', form=form, legend='New-Blog')



