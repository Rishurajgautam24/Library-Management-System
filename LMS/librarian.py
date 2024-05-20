from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import requests
from flask_login import current_user, login_required
from flask_bcrypt import Bcrypt
from .models import User, Section, Book, BorrowRequest, Transaction
from . import db
from .graphs import *

# Create Blueprint for librarian
librarian = Blueprint("librarian", __name__)

# API URLs
url_user = "http://127.0.0.1:5000/api/user"
url_book = "http://127.0.0.1:5000/api/book"
url_section = "http://127.0.0.1:5000/api/section"

# ============= Dashboard ===============
@librarian.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role == 1:
        if request.method == 'GET':
            # Fetch user data
            response = requests.get(url_user)
            data = response.json()

            # Generate data for graphs
            book_availablity_chart()
            transaction_history()
            borrow_request_status()
            section_wise_book_count()

            # Book stats
            book_count = Book.query.count()
            issued_books = Transaction.query.count()
            requested_books = BorrowRequest.query.filter_by(status="Pending").count()

            # Handle messages
            message = request.args.get('message')
            message_type = request.args.get('type')
            if message:
                return render_template("librarian/dashboard.html", user=current_user, data=data, book_count=book_count, issued_books=issued_books, requested_books=requested_books, message=message, type=message_type or "info")
            
            return render_template("librarian/dashboard.html", user=current_user, data=data, book_count=book_count, issued_books=issued_books, requested_books=requested_books)

# ============= Books ===============
@librarian.route('/view_books', methods=['GET', 'POST'])
@login_required
def view_books():
    if current_user.role == 1:
        if request.method == 'GET':
            # Fetch book data
            response = requests.get(url_book)
            data = response.json()

            # Handle messages
            message = request.args.get('message')
            message_type = request.args.get('type')
            if message:
                return render_template("librarian/books/view_books.html", user=current_user, books=data, message=message, type=message_type or "info")
            
            return render_template("librarian/books/view_books.html", user=current_user, books=data)

@librarian.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role == 1:
        if request.method == "GET":
            # Fetch section data
            response = requests.get(url_section)
            data = response.json()
            return render_template("librarian/books/add_book.html", sections=data)
        
        if request.method == "POST":
            # Add new book
            name = request.form.get("book_name")
            author = request.form.get("author")
            isbn = request.form.get("isbn")
            content = request.form.get('ckeditor')
            section_name = request.form.get("section_name")
            section = Section.query.filter_by(name=section_name).first()
            new_book = Book(name=name, author=author, isbn=isbn, content=content, section_id=section.id)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('librarian.view_books', message="Book added successfully", type="success"))

@librarian.route('/edit_book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    if current_user.role == 1:
        if request.method == "GET":
            # Fetch book and section data
            response1 = requests.get(url_book + f"/{id}")
            data1 = response1.json()
            response = requests.get(url_section)
            data = response.json()
            return render_template("librarian/books/edit_book.html", book=data1, sections=data)
        
        if request.method == "POST":
            # Update book details
            name = request.form.get("book_name")
            author = request.form.get("author")
            isbn = request.form.get("isbn")
            content = request.form.get('ckeditor')
            section_id = request.form.get("section_id")
            available = request.form.get("available")
            book = Book.query.get(id)
            book.name = name
            book.author = author
            book.isbn = isbn
            book.content = content
            book.section_id = section_id
            book.available = available == "True"
            db.session.commit()
            return redirect(url_for('librarian.view_books', message="Book updated successfully", type="success"))

@librarian.route('/delete_book/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_book(id):
    if current_user.role == 1:
        if request.method == "GET":
            # Delete book
            book = Book.query.get(id)
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for('librarian.view_books', message="Book deleted successfully", type="success"))

# ============= Sections ===============
@librarian.route('/view_sections', methods=['GET', 'POST'])
@login_required
def view_sections():
    if current_user.role == 1:
        if request.method == 'GET':
            # Fetch section data
            response = requests.get(url_section)
            data = response.json()

            # Handle messages
            message = request.args.get('message')
            message_type = request.args.get('type')
            if message:
                return render_template("librarian/sections/view_sections.html", user=current_user, sections=data, message=message, type=message_type or "info")
            
            return render_template("librarian/sections/view_sections.html", user=current_user, sections=data)

@librarian.route('/add_section', methods=['GET', 'POST'])
@login_required
def add_section():
    if current_user.role == 1:
        if request.method == "GET":
            message = request.args.get('message')
            return render_template("librarian/sections/add_section.html", message=message)
        
        if request.method == "POST":
            # Add new section
            name = request.form.get("section_name")
            description = request.form.get("description")
            section = Section.query.filter_by(name=name).first()
            if section:
                return redirect(url_for('librarian.add_section', message="Section already exists"))
            else:
                new_section = Section(name=name, description=description)
                db.session.add(new_section)
                db.session.commit()
                return redirect(url_for('librarian.view_sections', message="Section added successfully", type="success"))

@librarian.route('/edit_section/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_section(id):
    if current_user.role == 1:
        if request.method == "GET":
            # Fetch section data
            section = Section.query.get(id)
            return render_template("librarian/sections/edit_section.html", section=section)
        
        if request.method == "POST":
            # Update section details
            name = request.form.get("section_name")
            description = request.form.get("description")
            section = Section.query.get(id)
            section.name = name
            section.description = description
            db.session.commit()
            return redirect(url_for('librarian.view_sections', message="Section updated successfully", type="success"))

@librarian.route('/delete_section/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_section(id):
    if current_user.role == 1:
        if request.method == "GET":
            # Delete section
            section = Section.query.get(id)
            db.session.delete(section)
            db.session.commit()
            return redirect(url_for('librarian.view_sections', message="Section deleted successfully", type="success"))

# ============= Users ===============
@librarian.route('/view_users', methods=['GET', 'POST'])
@login_required
def view_users():
    if current_user.role == 1:
        if request.method == 'GET':
            # Fetch user data
            response = requests.get(url_user)
            data = response.json()

            # Handle messages
            message = request.args.get('message')
            message_type = request.args.get('type')
            if message:
                return render_template("librarian/users/view_users.html", user=current_user, users=data, message=message, type=message_type or "info")
            
            return render_template("librarian/users/view_users.html", user=current_user, users=data)

@librarian.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role == 1:
        if request.method == "GET":
            return render_template("librarian/users/add_user.html")
        
        if request.method == "POST":
            # Add new user
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role")
            user = User.query.filter_by(email=email).first()
            if user:
                return render_template("librarian/users/add_user.html", message="User already exists")
            else:
                new_user = User(username=username, email=email, password=password, role=role)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('librarian.view_users', message="User added successfully", type="success"))

@librarian.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role == 1:
        if request.method == "GET":
            # Fetch user data
            user = User.query.get(id)
            return render_template("librarian/users/edit_user.html", user=user)
        
        if request.method == "POST":
            # Update user details
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            role = request.form.get("role")
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            gender = request.form.get("gender")
            contact_no = request.form.get("contact_no")

            user = User.query.get(id)
            user.username = username
            user.email = email
            user.role = role
            user.fname = fname
            user.lname = lname
            user.gender = gender
            user.contact_no = contact_no

            if password and password == confirm_password:
                # Encrypt and update password
                user.password = Bcrypt().generate_password_hash(password).decode('utf-8')
            
            db.session.commit()
            return redirect(url_for('librarian.view_users', message="User updated successfully", type="success"))

@librarian.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if current_user.role == 1:
        if request.method == "GET":
            # Delete user
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('librarian.view_users', message="User deleted successfully", type="success"))

@librarian.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.logout'))

# ============== Request Handler ===============
@librarian.route('/requested-books', methods=['GET', 'POST'])
@login_required
def requested_books():
    if current_user.role == 1:
        if request.method == 'GET':
            # Fetch requested books
            requested_books = BorrowRequest.query.filter_by(status="Pending").all()
            return render_template("librarian/requests/requested_books.html", user=current_user, books=requested_books)

@librarian.route('/approve-request/<int:id>', methods=['GET', 'POST'])
@login_required
def approve_request(id):
    if current_user.role == 1:
        if request.method == 'GET':
            # Approve borrow request
            requested = BorrowRequest.query.get(id)
            requested.status = "Approved"
            book = Book.query.get(requested.book_id)
            book.available = False

            # Reject other requests for the same book
            requests_book = BorrowRequest.query.filter_by(book_id=requested.book_id).all()
            for req in requests_book:
                if req.id != requested.id:
                    req.status = "Rejected"

            # Create transaction record
            new_transaction = Transaction(book_id=requested.book_id, user_id=requested.user_id, borrowed_date=requested.request_date, returning_date=requested.return_date)
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('librarian.requested_books', message="Request approved successfully", type="success"))

@librarian.route('/reject-request/<int:id>', methods=['GET', 'POST'])
@login_required
def reject_request(id):
    if current_user.role == 1:
        if request.method == 'GET':
            # Reject borrow request
            requested = BorrowRequest.query.get(id)
            requested.status = "Rejected"
            db.session.commit()
            return redirect(url_for('librarian.requested_books', message="Request rejected successfully", type="success"))

@librarian.route('/approved-books', methods=['GET', 'POST'])      
@login_required
def approved_books():
    if current_user.role == 1:
        if request.method == 'GET':
            # Fetch approved books and downloads
            approved_books = Transaction.query.all()
            download_books = Download.query.all()
            return render_template("librarian/requests/approved_books.html", user=current_user, books=approved_books, downloads=download_books)

@librarian.route('/revoke/<int:id>', methods=['GET', 'POST'])
@login_required
def revoke(id):
    if current_user.role == 1:
        if request.method == 'GET':
            # Revoke book
            transaction = Transaction.query.get(id)
            book = Book.query.get(transaction.book_id)
            book.available = True
            db.session.delete(transaction)

            borrow_request = BorrowRequest.query.filter_by(book_id=transaction.book_id, user_id=transaction.user_id).first()
            borrow_request.status = "Revoked"
            
            download = Download.query.filter_by(book_id=transaction.book_id, user_id=transaction.user_id).first()
            if download:
                db.session.delete(download)
            
            db.session.commit()
            return redirect(url_for('librarian.approved_books', message="Book revoked successfully", type="success"))

@librarian.route('/search-book', methods=['GET', 'POST'])
@login_required
def search_book():
    if current_user.role == 1:
        if request.method == 'POST':
            # Search for books by name or author
            search = request.form.get("search")
            books = Book.query.filter(Book.name.like('%' + search + '%')).all()
            if books:
                return render_template("librarian/search_book.html", books=books, user=current_user)
            
            books = Book.query.filter(Book.author.like('%' + search + '%')).all()
            if books:
                return render_template("librarian/search_book.html", books=books, user=current_user)
            
            return redirect(url_for('librarian.dashboard', message="No books found", type="danger"))

@librarian.route('/search-user', methods=['GET', 'POST'])
@login_required
def search_user():
    if current_user.role == 1:
        if request.method == 'POST':
            # Search for users by username or email
            search = request.form.get("search")
            users = User.query.filter(User.username.like('%' + search + '%')).all()
            if users:
                return render_template("librarian/search_users.html", users=users, user=current_user)
            
            users = User.query.filter(User.email.like('%' + search + '%')).all()
            if users:
                return render_template("librarian/search_users.html", users=users, user=current_user)
            
            return redirect(url_for('librarian.dashboard', message="No users found", type="danger"))

@librarian.route('/search-sections', methods=['GET', 'POST'])
@login_required
def search_section():
    if current_user.role == 1:
        if request.method == 'POST':
            # Search for sections by name
            search = request.form.get("search")
            sections = Section.query.filter(Section.name.like('%' + search + '%')).all()
            if sections:
                return render_template("librarian/search_sections.html", sections=sections, user=current_user)
            
            return redirect(url_for('librarian.dashboard', message="No sections found", type="danger"))

# Auto revoke books not returned in time
@librarian.route('/auto-revoke', methods=['GET', 'POST'])
def auto_revoke():
    transactions = Transaction.query.all()
    for transaction in transactions:
        if transaction.returning_date < datetime.today().date():
            book = Book.query.get(transaction.book_id)
            book.available = True
            db.session.delete(transaction)
            borrow_request = BorrowRequest.query.filter_by(book_id=transaction.book_id, user_id=transaction.user_id).first()
            borrow_request.status = "Revoked"
            download = Download.query.filter_by(book_id=transaction.book_id, user_id=transaction.user_id).first()
            if download:
                db.session.delete(download)
            db.session.commit()
    return redirect(url_for('librarian.dashboard', message="Books revoked successfully", type="success"))

# Grant permission to download book
@librarian.route('/download/<int:id>', methods=['GET', 'POST'])
@login_required
def download(id):
    if current_user.role == 1:
        transaction = Transaction.query.filter_by(id=id).first()
        new_download = Download(book_id=transaction.book_id, user_id=transaction.user_id, permission=True)
        db.session.add(new_download)
        db.session.commit()
        return redirect(url_for('librarian.approved_books', message="Permission granted successfully", type="success"))

@librarian.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if current_user.role == 1:
        if request.method == 'GET':
            feedbacks = Feedback.query.all()
            return render_template("librarian/feedbacks.html", user=current_user, feedbacks=feedbacks)
