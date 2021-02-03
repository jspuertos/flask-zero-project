from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Event
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/events')
@login_required
def events():
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id)
    return render_template('events.html', email=current_user.email, events=events)
