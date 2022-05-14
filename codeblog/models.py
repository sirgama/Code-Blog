from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from codeblog import db, login_manager, app
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    blog = db.relationship('Blog', backref='author', lazy=True)
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    




    def __repr__(self):
            return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='blog', lazy='dynamic')
    


    def __repr__(self):
            return f"Blog('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) 
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'),nullable=False)
    comment = db.Column(db.String(100))

    def __repr__(self):
            return f"Comment('{self.comment}')"
        
    
