from passlib.context import CryptContext
from sqlalchemy.ext.hybrid import hybrid_property
from . import db, app

app.app_context().push()

class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_out = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.title}, {self.author_id}, {self.description}, {self.is_out}"

class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"Author('{self.name}')"

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    _password = db.Column("password", db.String(128))

    # Defining CryptContext
    pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Defining hybrid property for set/get of _password (private attribute).
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, plaintext_password):
        self._password = self.pswd_context.hash(plaintext_password)

    def verifyPassword(self, plaintext_password):
        # True or False
        return self.pswd_context.verify(plaintext_password, self._password)
    
    def __repr__(self) -> str:
        return f"User('{self.name}')"
    

class Checkout(db.Model):
    __tablename__ = "checkouts"
    checkout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    def __repr__(self) -> str:
        return f"Checkout('{self.user_id}', '{self.book_id}', '{self.checkout_date}', '{self.return_date}')"
    
db.create_all()