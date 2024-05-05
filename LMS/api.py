from flask_restful import Resource, fields, marshal_with, reqparse
from .models import db, User, Section, Book
from .validation import NotFoundError, AlreadyExistsError, ValidationError
from datetime import datetime ,timedelta
from flask_bcrypt import Bcrypt
# Define fields for marshalling
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'role': fields.String,
    'fname': fields.String,
    'lname': fields.String,
    'email': fields.String,
    'gender': fields.String,
    'contact_no': fields.String,
    'created_date': fields.DateTime(dt_format='iso8601'),
    'updated_date': fields.DateTime(dt_format='iso8601')
}

section_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_date': fields.DateTime(dt_format='iso8601'),
    'description': fields.String,
    'updated_date': fields.DateTime(dt_format='iso8601')
}

book_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'isbn': fields.String,
    'content': fields.String,
    'author': fields.String,
    'available': fields.Boolean,
    'section_id': fields.Integer,
    'section_name': fields.String(attribute=lambda x: x.section.name if x.section else None),
}


transaction_fields = {
    'id': fields.Integer,
    'book_id': fields.Integer,
    'user_id': fields.Integer,
    'borrowed_date': fields.DateTime(dt_format='iso8601'),
    'returning_date': fields.DateTime(dt_format='iso8601'),
    'returned_date': fields.DateTime(dt_format='iso8601'),
    'returned': fields.Boolean
}

# Create a RequestParser instance
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('role', type=str, required=True, help='Role is required')
user_parser.add_argument('fname', type=str, required=False, help='First name is required')
user_parser.add_argument('lname', type=str, required=False, help='Last name is required')
user_parser.add_argument('email', type=str, required=False, help='Email is required')
user_parser.add_argument('gender', type=str, required=False, help='Gender is required')
user_parser.add_argument('contact_no', type=str, required=False, help='Contact number is required')

# Create a RequestParser instance
section_parser = reqparse.RequestParser()
section_parser.add_argument('name', type=str, required=True, help='Name is required')
section_parser.add_argument('description', type=str, required=False, help='Description is optional')

book_parser = reqparse.RequestParser()
book_parser.add_argument('name', type=str, required=True, help='Name is required')
book_parser.add_argument('author', type=str, required=True, help='Author is required')
book_parser.add_argument('isbn', type=str, required=True, help='ISBN is required')
book_parser.add_argument('available', type=bool, required=False, help='Available is optional')


class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self, id=None):
        if id:
            user = User.query.get(id)
            if not user:
                raise NotFoundError(status_code=404)
            return user
        else:
            users = User.query.all()
            return users

    @marshal_with(user_fields)
    def post(self):
        # Parse the incoming JSON data
        user_parser.add_argument('password', type=str, required=True, help='Password is required')
        user_parser.add_argument('confirm_password', type=str, required=True, help='Confirm password is required')
        args = user_parser.parse_args()
        username = args['username']
        password = args['password']
        confirm_password = args['confirm_password']
        role = args['role']

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            raise AlreadyExistsError(status_code=400)
        
        if password != confirm_password:
            raise ValidationError(status_code=400, error='Password and Confirm Password do not match')

        password = Bcrypt().generate_password_hash(password).decode('utf-8')
        # Create a new user instance
        new_user = User(username=username, password=password, role=role,
                        fname=args.get('fname'), lname=args.get('lname'),
                        email=args.get('email'), gender=args.get('gender'),
                        contact_no=args.get('contact_no'))
        db.session.add(new_user)
        db.session.commit()

        return new_user, 201

    @marshal_with(user_fields)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            raise NotFoundError(status_code=404)

        # Parse the arguments and update the user instance accordingly
        args = user_parser.parse_args()
        user.username = args.get('username', user.username)
        user.role = args.get('role', user.role)
        user.fname = args.get('fname', user.fname)
        user.lname = args.get('lname', user.lname)
        user.email = args.get('email', user.email)
        user.gender = args.get('gender', user.gender)
        user.contact_no = args.get('contact_no', user.contact_no)
        user.updated_date = datetime.utcnow()

        db.session.commit()

        return user

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            raise NotFoundError(status_code=404)
        db.session.delete(user)
        db.session.commit()

        return '', 204


class SectionAPI(Resource):
    @marshal_with(section_fields)
    def get(self, id=None):
        if id:
            section = Section.query.get(id)
            if not section:
                raise NotFoundError(status_code=404)
            return section
        else:
            sections = Section.query.all()
            return sections

    @marshal_with(section_fields)
    def post(self):
        # Parse the incoming JSON data
        args = section_parser.parse_args()
        name = args['name']
        description = args['description']

        # Check if the section name already exists
        if Section.query.filter_by(name=name).first():
            raise AlreadyExistsError(status_code=400)

        # Create a new section instance
        new_section = Section(name=name, description=description)
        db.session.add(new_section)
        db.session.commit()

        return "" ,201

    @marshal_with(section_fields)
    def put(self, id):
        section = Section.query.get(id)
        if not section:
            raise NotFoundError(status_code=404)

        args = section_parser.parse_args()
        section.name = args.get('name', section.name)
        section.description = args.get('description', section.description)
        section.updated_date = datetime.utcnow()

        db.session.commit()

        return section

    def delete(self, id):
        section = Section.query.get(id)
        if not section:
            raise NotFoundError(status_code=404)

        db.session.delete(section)
        db.session.commit()

        return '', 204
    

class BookAPI(Resource):
    @marshal_with(book_fields)
    def get(self, id=None):
        if id:
            book = Book.query.get(id)
            if not book:
                raise NotFoundError(status_code=404)
            return book
        else:
            books = Book.query.all()
            if not books:
                raise NotFoundError(status_code=404)
            return books

    @marshal_with(book_fields)
    def post(self):
        book_parser.add_argument('content', type=str, required=True, help='Content is required')
        book_parser.add_argument('section_id', type=int, required=True, help='Section ID is required')
        # Parse the incoming JSON data
        args = book_parser.parse_args()
        name = args['name']
        isbn = args['isbn']
        content = args['content']
        author = args['author']
        available = args.get('available', True)
        section_id = args['section_id']

        # Check if the name and section exists
        if Book.query.filter_by(name=name ,author=author).first():
            raise AlreadyExistsError(status_code=400)

        # Create a new book instance
        new_book = Book(name=name,isbn=isbn, content=content, author=author,
                        section_id=section_id,
                        available=available)
        db.session.add(new_book)
        db.session.commit()

        return new_book, 201

    @marshal_with(book_fields)
    def put(self, id):
        book = Book.query.get(id)
        if not book:
            raise NotFoundError(status_code=404)

        # Parse the arguments and update the book instance accordingly
        args = book_parser.parse_args()
        book.name = args.get('name', book.name)
        book.isbn = args.get('isbn', book.isbn)
        book.content = args.get('content', book.content)
        book.author = args.get('author', book.author)
        book.available = args.get('available', book.available)
        book.section_id = args.get('section_id', book.section_id)

        db.session.commit()

        return book

    def delete(self, id):
        book = Book.query.get(id)
        if not book:
            raise NotFoundError(status_code=404)

        db.session.delete(book)
        db.session.commit()

        return '', 204
    