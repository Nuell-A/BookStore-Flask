from . import db, app
from .models import Book, Author, User, Checkout
from datetime import datetime
from sqlalchemy.sql.expression import func
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

    # I'm not sure of description and is_out were passed.
    book = Book(title=title, author_id=author.author_id, description=description, is_out=is_out)
    db.session.add(book)
    db.session.commit()

    print("Book entry created.")

def getRandBooks(no_rows: int):
    random_books = db.session.query(Book.title, Book.author_id, Book.description).order_by(func.random()).limit(no_rows).all()
    
    random_books_finished = []
    for title, author_id, description in random_books:
        author = Author.query.filter_by(author_id=author_id).first()
        author_name = author.name
        random_books_finished.append((title, author_name, description))

    print(random_books_finished)
    return random_books_finished

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

def createCheckout(user_name: str, book_title: str):
    '''Sets checkout date and grabs instances of User and Book for ID. Adds it'''
    checkout_date = datetime.now()
    user = User.query.filter_by(name=user_name).first()
    book = Book.query.filter_by(title=book_title).first()

    checkout = Checkout(user_id=user.id, book_id=book.id, checkout_date=checkout_date)
    db.session.add(checkout)
    db.session.commit()

'''with open('app\\static\\assets\\testbooks.csv') as file:
    file_reader = csv.reader(file, delimiter=",")
    for row in file_reader:
        title = row[0]
        author = row[1]
        description = row[2]
        is_out = checkBool(row[3])
        
        createBook(title, author, description=description, is_out=is_out)'''