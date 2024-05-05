from .models import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import base64


matplotlib.use('Agg') 

def format_pct_and_count(pct, allvals):
    absolute = int(pct / 100. * sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def book_availablity_chart():
    books = Book.query.all()
    available = 0
    not_available = 0
    for book in books:
        if book.available==True:
            available += 1
        else:
            not_available += 1
    labels = ['Available', 'Not Available']
    sizes = [available, not_available]
    plt.title('Book Available VS Not Available')
    colors = ['gold', 'yellowgreen']
    explode = (0.1, 0) # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('LMS/static/images/book_availablity.png')
    plt.close()
    return 'LMS/static/images/book_availablity.png'

def transaction_history():
    transactions = Transaction.query.all()
    dates = []
    for transaction in transactions:
        dates.append(transaction.borrowed_date)
    dates.sort()
    date_dict = {}
    for date in dates:
        if date in date_dict:
            date_dict[date] += 1
        else:
            date_dict[date] = 1
    x = []
    y = []
    for key, value in date_dict.items():
        x.append(key)
        y.append(value)
    plt.plot(x, y)
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.ylabel('Number of Transactions')
    plt.title('Transaction History')
    plt.savefig('LMS/static/images/transaction_history.png')
    plt.close()
    return 'LMS/static/images/transaction_history.png'


def borrow_request_status():
    borrow_requests = BorrowRequest.query.all()
    pending = 0
    approved = 0
    rejected = 0
    revoked = 0
    for borrow_request in borrow_requests:
        if borrow_request.status == 'Pending':
            pending += 1
        elif borrow_request.status == 'Approved':
            approved += 1
        elif borrow_request.status == 'Rejected':
            rejected += 1
        elif borrow_request.status == 'Revoked':
            revoked += 1
    labels = ['Pending', 'Approved', 'Rejected', 'Revoked']
    sizes = [pending, approved, rejected, revoked]
    # title
    plt.title('Borrow Request Status')
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0) # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('LMS/static/images/borrow_request_status.png')
    plt.close()
    return 'LMS/static/images/borrow_request_status.png'


def section_wise_book_count():
    sections = Section.query.all()
    section_names = []
    book_counts = []
    for section in sections:
        section_names.append(section.name)
        book_counts.append(len(section.books))
    y_pos = np.arange(len(section_names))
    plt.bar(y_pos, book_counts, align='center', alpha=0.5)
    plt.xticks(y_pos, section_names)
    plt.ylabel('Number of Books')
    plt.title('Section-wise Book Count')
    plt.savefig('LMS/static/images/section_wise_book_count.png')
    plt.close()
    return 'LMS/static/images/section_wise_book_count.png'

def user_role_distribution():
    users = User.query.all()
    librarians = 0
    users_count = 0
    for user in users:
        if user.role == 1:
            librarians += 1
        else:
            users_count += 1
    labels = ['Librarians', 'Users']
    sizes = [librarians, users_count]
    # title
    plt.title('User Role Distribution')
    colors = ['gold', 'yellowgreen']
    explode = (0.1, 0) # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('LMS/static/images/user_role_distribution.png')
    plt.close()
    return 'LMS/static/images/user_role_distribution.png'









