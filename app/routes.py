from flask import redirect, render_template, request, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from . import app, controller

# Create login manager and give it the app context
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    search_results = controller.getRandBooks(3)
    context = {
        "search": search,
        "search_results": search_results
    }
    return render_template('home.html', context=context)

@app.route('/add-to-cart', methods=['POST'])
def addToCart():
    data = request.json
    print(data)
    book = {
        'book_title': data['book_title'], 
        'book_author': data['book_author'], 
        'book_description': data['book_description']
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

@app.route('/checkout')
def checkout():
    cart = session.pop('cart', [])
    # Process checkout, update database, etc.
    return 'Checkout complete'

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

@app.route('/account/create')
def accountCreate():
    return render_template('account_create.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user.id)