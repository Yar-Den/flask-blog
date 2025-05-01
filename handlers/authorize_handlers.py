from flask import render_template, redirect, request, url_for, flash
from models import db, User
from flask_login import login_user, logout_user


def handle_login():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and User.check_password(user.password, password):
            login_user(user)
            return redirect(url_for('read'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


def handle_regiter():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        email = request.form['email']

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken', 'danger')
        else:
            password_hash = User.password_hash(password)
            new_user = User(username=username,
                            password_hash=password_hash,
                            email=email
                            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully', 'success')
            login_user(new_user)
            return redirect(url_for('read'))
    return render_template('register.html')


def handle_logout():
    logout_user()
    return redirect(url_for('index'))
