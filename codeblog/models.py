from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.Date(timezone=True), default=func.now())
