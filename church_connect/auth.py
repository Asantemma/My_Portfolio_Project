# auth.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('auth.register'))
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists. Please choose a different one.', 'error')
            return redirect(url_for('auth.register'))

        # Hash the password before storing in the database
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Create a new user instance
        new_user = User(username=username, email=email, password=hashed_password)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created successfully. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Find user by username
        user = User.query.filter_by(username=username).first()

        # Check if user exists and if password is correct
        if user and check_password_hash(user.password, password):
            # Log the user in
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
