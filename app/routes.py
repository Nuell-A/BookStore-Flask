from flask import redirect, render_template, request, url_for, flash
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

@app.route('/cart')
def cart():
    items_in_cart = ["Lion King", "Spirit of the Stallion", "Suuuppppperrrrr long name for testing purposes"]
    context = {
        "items_in_cart": items_in_cart
    }
    return render_template('cart.html', context=context)

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