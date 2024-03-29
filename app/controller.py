from . import db, app
from .models import Book, Author, User, Checkout
from datetime import datetime
from sqlalchemy.sql.expression import func
from sqlalchemy import or_
import csv # Only needed sometimes when inputting test data. 

app.app_context().push()

def createBook(title: str, author_name: str, **kwargs):
    '''Checks if author exists. If author doesn't exists, it will create
    new author instance for use. Next it checks if the optional kwargs were passed
    and adds the book.'''
    # Checks if author is already in databse, if not it creates new instance.
    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

    # Checks if optional parameters were passed or not. 
    description = kwargs.get('description') # Can be null
    is_out = kwargs.get('is_out') # Default False

    # Creates entry, adds, and commits.
    book = Book(title=title, author_id=author.author_id, description=description, is_out=is_out)
    db.session.add(book)
    db.session.commit()

    print("Book entry created.")

def getRandBooks(no_rows: int):
    '''Gets random x amount of rows.'''
    # Queries db for rows (only books that are not checked out)
    random_books = db.session.query(Book.title, Book.author_id, Book.description).filter(Book.is_out==False).order_by(func.random()).limit(no_rows).all()
    
    # List for row of books but with author name in place of author id.
    random_books_finished = []
    for title, author_id, description in random_books:
        author = Author.query.filter_by(author_id=author_id).first()
        author_name = author.name
        random_books_finished.append((title, author_name, description))
    return random_books_finished

def searchBooks(search: str):
    '''Searches the database for books similar to search string from user.'''
    # Using or_ from sqlalchemy to utilize OR statement in MySQL. Also joining Author table to access column (author name) and use it in HTML
    search_results = db.session.query(Book, Author.name).join(Author, Book.author_id == Author.author_id).filter(or_(Book.title.ilike(f'%{search}%'), Author.name.ilike(f'%{search}%'), Book.description.ilike(f'%{search}%')), Book.is_out==False).all()
    return search_results

def checkUserBooks(user: str):
    user = User.query.filter_by(name=user).first()
    checked_out_books = (
        db.session.query(Book, Author.name)
        .join(Checkout, Book.book_id == Checkout.book_id)
        .join(Author, Book.author_id == Author.author_id)
        .filter(Checkout.user_id == user.user_id)
        .all()
    )

    return checked_out_books

def checkBool(is_out):
    '''Created to check if string from CSV file is True/False.'''
    if is_out == "False":
        return False
    elif is_out == "True":
        return True

def createAuthor(name: str):
    '''Creates author'''
    author = Author(name=name)
    db.session.add(author)
    db.session.commit()

def createUser(name: str, plaintext_pwrd: str):
    '''Creates user and set password'''
    user = User(name=name)
    user.password = plaintext_pwrd
    db.session.add(user)
    db.session.commit()

def checkUser(email: str, plaintext_pwrd: str):
    '''Queries database for the email input. If there is a match, 
    then it tests the plaintext against the hashed in the database.'''
    user = User.query.filter_by(name=email).first()
    if not user:
        print(f"No user account for {email} found.")
        return False
    
    if user.verifyPassword(plaintext_pwrd):
        print("Successfully logged in.")
        return True
    else:
        print("Check credentials and try again.")
        return False

def createCheckout(user_name: str, book_title: str, book_author: str):
    '''Sets checkout date and grabs instances of User and Book for ID. Adds it'''
    checkout_date = datetime.now()
    user = User.query.filter_by(name=user_name).first()
    author = Author.query.filter_by(name=book_author).first()
    book = Book.query.filter_by(title=book_title).filter_by(author_id=author.author_id).first()

    checkout = Checkout(user_id=user.user_id, book_id=book.book_id, checkout_date=checkout_date)
    checkoutBook(book.title, book.description)
    db.session.add(checkout)
    db.session.commit()

def checkoutBook(book_title: str, book_description: str):
    book = Book.query.filter_by(title=book_title).filter_by(description=book_description).first()
    book.is_out = True
    db.session.commit()

def checkinBook(book_title: str, book_description: str):
    book = Book.query.filter_by(title=book_title).filter_by(description=book_description).first()
    print(book)
    book.is_out = False
    db.session.commit()

def deleteCheckout(book_title: str, book_description: str, username: str):
        book = Book.query.filter_by(title=book_title).filter_by(description=book_description).first()
        user = User.query.filter_by(name=username).first()
        try:
            checkout_entry = (
                db.session.query(Checkout)
                .filter_by(user_id=user.user_id, book_id=book.book_id)
                .first()
            )
            if checkout_entry:
                db.session.delete(checkout_entry)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return False

'''with open('app\\static\\assets\\testbooks.csv') as file:
    file_reader = csv.reader(file, delimiter=",")
    for row in file_reader:
        title = row[0]
        author = row[1]
        description = row[2]
        is_out = checkBool(row[3])
        
        createBook(title, author, description=description, is_out=is_out)'''