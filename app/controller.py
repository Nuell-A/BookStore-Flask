from . import db, app
from .models import Book, Author, User, Checkout
from datetime import datetime

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

def createCheckout(user_name: str, book_title: str):
    '''Sets checkout date and grabs instances of User and Book for ID. Adds it'''
    checkout_date = datetime.now()
    user = User.query.filter_by(name=user_name).first()
    book = Book.query.filter_by(title=book_title).first()

    checkout = Checkout(user_id=user.id, book_id=book.id, checkout_date=checkout_date)
    db.session.add(checkout)
    db.session.commit()