from flask  import Blueprint, render_template
from . import db
from .models import User

views = Blueprint("views", __name__)


@views.route("/home")
def home():
    return render_template('home.html')