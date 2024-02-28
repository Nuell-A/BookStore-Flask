from flask import redirect, render_template, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from . import app, controller

# Create login manager and give it the app context
login_manager = LoginManager()
login_manager.init_app(app)
# Mock DB while I migrate SQL database to server (instead of laptop).
users = {
    "nuell01@test.com": {"email": "nuell01@test.com", "password": "password1"},
    "nuell02@test.com": {"email": "nuell02@test.com", "password": "password2"},
}

@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    search_results = ["Lion King", "Spirit of the Stallion", "Suuuppppperrrrr long name for testing purposes"]
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
        
@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(controller.checkUser(email, password))
        '''if user and user['password'] == password:
            login_user(User(email))
            flash("Logged in successfully.")
            return redirect(url_for('profile'))'''
        
    return render_template('account.html')

@app.route('/account/create')
def accountCreate():
    return render_template('account_create.html')

@app.route('/profile')
def profile():
    return render_template('account_create.html')