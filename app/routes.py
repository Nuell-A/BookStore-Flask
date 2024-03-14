from flask import redirect, render_template, request, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from . import app, controller
import json

# Create login manager and give it the app context
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    random_results = controller.getRandBooks(3)
    search_results = []

    # If user searches for something, query database.
    if search:
        search_results = controller.searchBooks(search)

    context = {
        "search": search,
        "search_results": search_results,
        "random_results": random_results,
    }
    return render_template('home.html', context=context)

@app.route('/add-to-cart', methods=['POST'])
def addToCart():
    data = request.json
    book = {
        "book_title": data['book_title'], 
        "book_author": data['book_author'], 
        "book_description": data['book_description']
    }
    print(book)
    cart = session.get('cart', [])
    cart.append(book)
    session['cart'] = cart

    return "Book added to cart", 200

@app.route('/cart')
def cart():
    items_in_cart = session.get('cart', [])
    print(items_in_cart)
    recommended_books = controller.getRandBooks(4)
    context = {
        "items_in_cart": items_in_cart,
        "recommended_books": recommended_books,
    }
    return render_template('cart.html', context=context)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    json_prep = data['books_in_cart']
    json_format = json_prep.replace("'", '"')
    books_in_cart = json.loads(json_format)
    print(books_in_cart)
    for item in books_in_cart:
        book_title = item['book_title']
        book_author = item['book_author']
        controller.createCheckout(current_user.id, book_title, book_author)

    cart = session.pop('cart', [])
    # Process checkout, update database, etc.
    return 'Checkout complete', 200

@app.route('/thank-you')
def thankYou():
    return render_template('thank_you.html')

# Represents User object.
class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def loadUser(user_id):
    return User(user_id)
        
@app.route('/account-login', methods=['GET', 'POST'])
def accountLogin():
    '''If request is POST, it checks if login credentials were correct'''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        is_correct = controller.checkUser(email, password)
        if is_correct:
            print("Redirecting URL")
            login_user(User(email))
            flash("Logged in successfully.")
            return redirect(url_for('profile'))
        else:
            flash("Check your credentials.")
            return redirect(url_for('accountLogin'))
    return render_template('account_login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out!")
    return redirect(url_for('accountLogin'))

@app.route('/account/create', methods=['GET', 'POST'])
def accountCreate():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            controller.createUser(email, password)
            print(f"User {email} created")
            return redirect(url_for('accountLogin'))
        except:
            print("Error creating account")
            return redirect(url_for('accountCreate'))
    return render_template('account_create.html')

@app.route('/profile')
@login_required
def profile():
    print(current_user.id)
    return render_template('profile.html', user=current_user.id)
