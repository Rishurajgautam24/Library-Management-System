from flask import Blueprint, render_template, request, jsonify, redirect, url_for, make_response
import requests
from flask_login import current_user
from .models import User, Book, Section, BorrowRequest, Transaction,Download,Feedback
from . import db
from flask_login import login_required
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta



url_book ="http://127.0.0.1:5000/api/book"

user = Blueprint("user", __name__)

@user.route('/dashboard', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def dashboard():
    url="http://127.0.0.1:5000/api/book"
    if request.method == 'GET':
        response = requests.get(url)
        data = response.json()
        if request.args.get("message"):
            message = request.args.get("message")
            if request.args.get("type"):
                type = request.args.get("type")
                return render_template("user/dashboard.html", user=current_user, data=data, message=message, type=type)
            return render_template("user/dashboard.html", user=current_user, data=data, message=message)
        return render_template("user/dashboard.html", user=current_user, data=data)


@user.route('/logout')
@login_required
def logout():
    return render_template("login.html")

#  edit profile 
@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'GET':
        user = current_user
        user = User.query.filter_by(id=user.id).first()
        return render_template("user/edit_profile.html", user=user)
    if request.method == "POST":
        id = current_user.id
        username = request.form.get("username")
        email = request.form.get("email")
        if request.form.get("password"):
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            if password != confirm_password:
                user = User.query.filter_by(id=id).first()
                return render_template("user/edit_profile.html", message="Passwords do not match",user=user)
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        gender = request.form.get("gender")
        contact_no = request.form.get("contact_no")

        # update existing data in database
        user = User.query.get(id)
        user.username = username
        user.email = email
        user.fname = fname
        user.lname = lname
        user.gender= gender
        user.contact_no = contact_no
        if request.form.get("password"):
            # encrypt password before saving
            password = Bcrypt().generate_password_hash(password).decode('utf-8')
            user.password = password
        db.session.commit()
        return redirect(url_for('user.dashboard', message="User updated successfully",type="success"))
    
# ========== Book Routes ==========

@user.route('/request-book/', methods=['GET', 'POST'])
@login_required
def request_book():
    if request.method == 'GET':
        owned_books=Transaction.query.filter_by(user_id=current_user.id).all()
        pending_requests=BorrowRequest.query.filter_by(user_id=current_user.id).filter_by(status="Pending").all()

        if len(pending_requests)>=5:
            return redirect(url_for('user.dashboard',message="You have reached the maximum limit of requests",type="danger",user=current_user))
        if len(owned_books)>=5:
            return redirect(url_for('user.dashboard',message="You have reached the maximum limit of books you can have",type="danger",user=current_user))
        
        books=Book.query.filter_by(available=True).all()
        recent_books=Book.query.filter_by(available=True).order_by(Book.id.desc()).limit(5).all()
        if request.args.get("message"):
            message = request.args.get("message")
            return render_template("user/request_book.html",books=books,user=current_user,recent_books=recent_books,message=message)
        return render_template("user/request_book.html",books=books,user=current_user,recent_books=recent_books)
    
@user.route('/request-book/<int:id>', methods=['GET', 'POST'])
@login_required
def request_book_id(id):
    if request.method == 'GET':
        book=Book.query.get(id)
        if book.available==False:
            return redirect(url_for('user.request_book',message="Book is not available",user=current_user))
        section=Section.query.filter_by(id=book.section_id).first()
        return render_template("user/requested_book.html",book=book,section=section,user=current_user)
    if request.method == 'POST':
        if request.form.get("days"):
            days=request.form.get("days")
            if days=="others":
                days=request.form.get("others") 
        book=Book.query.get(id)
        book_id=book.id
        user_id=current_user.id
        status="Pending"
        return_date=datetime.now()+timedelta(days=int(days))
        return_date=return_date.date()
        print(return_date)
        new_req=BorrowRequest(book_id=book_id,user_id=user_id,return_date=return_date,status=status)
        db.session.add(new_req)
        db.session.commit()
        return redirect(url_for('user.dashboard',message="Book requested successfully",type="success",user=current_user))

@user.route('/my-books/', methods=['GET', 'POST'])
@login_required
def my_books():
    if request.method == 'GET':
        owned_books=Transaction.query.filter_by(user_id=current_user.id).all()
        return render_template("user/my_books.html",books=owned_books,user=current_user)
    
@user.route('/return-book/<int:id>', methods=['GET', 'POST'])
@login_required
def return_book(id):
    book=Book.query.get(id)
    transaction=Transaction.query.filter_by(book_id=id).filter_by(user_id=current_user.id).first()
    db.session.delete(transaction)
    book.available=True
    db.session.commit()
    return redirect(url_for('user.my_books',message="Book returned successfully",type="success",user=current_user))


@user.route('read-book/<int:id>', methods=['GET', 'POST'])
@login_required
def read_book(id):
    book=Book.query.get(id)
    # check if the user has permission to download the book
    download=Download.query.filter_by(book_id=id).filter_by(user_id=current_user.id).first()
    if download:
        return render_template("user/read_book.html",book=book,user=current_user,permission=True)
    return render_template("user/read_book.html",book=book,user=current_user)

@user.route('/search-book', methods=['GET', 'POST'])
@login_required
def search_book():
    if request.method == 'POST':
        search=request.form.get("search")
        if search=="":
            return redirect(url_for('user.request_book',message="Please enter a search term",type="danger",user=current_user))
        # seach it in the database in name or in author and return the results
        books=Book.query.filter(Book.name.like('%'+search+'%')).all()
        if books:
            return render_template("user/search_book.html",books=books,user=current_user)
        books=Book.query.filter(Book.author.like('%'+search+'%')).all()
        if books:
            return render_template("user/search_book.html",books=books,user=current_user)
        return redirect(url_for('user.dashboard',message="No books found",type="danger",user=current_user))

# feedback 
@user.route('/feedback/<int:id>', methods=['GET', 'POST'])
@login_required
def feedback(id):
    if request.method == 'GET':
        book=Book.query.get(id)
        return render_template("user/feedback.html",book=book,user=current_user)
    if request.method == 'POST':
        rating=request.form.get("rating")
        feedback=request.form.get("feedback")
        book_id=id
        user_id=current_user.id
        new_feedback=Feedback(feedback=feedback,book_id=book_id,user_id=user_id)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(url_for('user.dashboard',message="Feedback submitted successfully",type="success",user=current_user))