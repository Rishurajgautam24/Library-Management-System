from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from .models import *
import requests


views = Blueprint("views", __name__)


@views.route("/")
def home():
    url ="http://127.0.0.1:5000/api/book"
    response = requests.get(url)
    books = response.json()
    return render_template("homepage.html",books=books, user=current_user)

@views.route("/login")
def login():
    return redirect(url_for('auth.login'))