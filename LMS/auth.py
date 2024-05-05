from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from flask_bcrypt import Bcrypt

from .models import db, User
import requests 


auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST', 'PUT', 'DELETE'])
def login():
    if request.method == 'GET':
        if request.args.get('message'):
            message = request.args.get('message')
            return render_template("login.html", message=message)
        return render_template("login.html")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role= request.form.get('role')
        user = User.query.filter_by(username=username).first()
        if user:
            if Bcrypt().check_password_hash(user.password, password):
                if role =="User" and user.role == 0:
                    login_user(user)
                    return redirect(url_for('user.dashboard'))
                elif role =="Admin" and user.role == 1:
                    login_user(user)
                    return redirect(url_for('librarian.dashboard'))
                else:
                    return redirect(url_for('auth.login', message="Invalid Role"))
            else:
                return redirect(url_for('auth.login', message="Invalid Password"))
        else:
            return redirect(url_for('auth.login', message="User not found"))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if request.args.get('message'):
            message = request.args.get('message')
            return render_template("signup.html", message=message)
        return render_template("signup.html")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        if role == "User":
            role = 0
        else:
            role = 1
        if password != confirm_password:
                return redirect(url_for('auth.signup', message="Password does not match"))
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('auth.signup', message="User already exists"))
        else:
            password = Bcrypt().generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",  message="User created successfully",type="success")
        
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home',message="Logout Successfully",type="success"))  # Redirect to homepage after logout


