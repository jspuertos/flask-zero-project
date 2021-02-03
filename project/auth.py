from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from .models import User, Event
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.events'))    

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/create-event')
@login_required
def createevent():
    return render_template('create-event.html')

@auth.route('/create-event', methods=['POST'])
@login_required
def createevent_post():
    event = request.form.get('event')
    category = request.form.get('category')
    location = request.form.get('location')
    address = request.form.get('address')
    initial_date = request.form.get('initial_date')
    final_date = request.form.get('final_date')
    attendance = request.form.get('attendance')

    user_id = current_user.id

    new_event = Event(event=event, category=category, location=location, address=address, initial_date=initial_date, final_date=final_date, attendance=attendance, user_id=user_id)

    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('main.events'))
