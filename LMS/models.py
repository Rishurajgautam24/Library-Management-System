from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)  
    fname = db.Column(db.String(100), nullable=True)
    lname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact_no = db.Column(db.String(15), nullable=True)
    created_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    updated_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())

    # Define relationships
    transactions = relationship('Transaction', backref='user', cascade='all, delete-orphan')
    borrow_requests_received = relationship('BorrowRequest', backref='recipient', cascade='all, delete-orphan')


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    description = db.Column(db.Text, nullable=True)
    updated_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())

    # Define relationships
    books = relationship('Book', backref='section', cascade='all, delete-orphan')



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    created_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    updated_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())

    # Define relationships
    transactions = relationship('Transaction', backref='book', cascade='all, delete-orphan')
    borrow_requests = relationship('BorrowRequest', backref='requested_book', cascade='all, delete-orphan')
    downloads = relationship('Download', backref='book_download', cascade='all, delete-orphan')
    feedbacks = relationship('Feedback', backref='book_feedbacks', cascade='all, delete-orphan')
    


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    borrowed_date = db.Column(db.Date, nullable=True, default=datetime.utcnow().date())
    returning_date = db.Column(db.Date, nullable=True)

    


class BorrowRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_date = db.Column(db.Date, nullable=True, default=datetime.utcnow().date())
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), nullable=False, default='Pending')

   # Define relationships
    user = relationship('User', backref='borrow_requests_details')
    book = relationship('Book', backref='borrow_requests_details')

# model for giving acess to user to download the book 
class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    permission = db.Column(db.Boolean, nullable=False, default=False)

    # Define relationships
    user = relationship('User', backref='downloaded_books')
    book = relationship('Book', backref='downloaded_books')

# model for storing the feedback on the book
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())

    # Define relationships
    user = relationship('User', backref='feedbacks_givenby')
    book = relationship('Book', backref='feedbacks_givenon')

   