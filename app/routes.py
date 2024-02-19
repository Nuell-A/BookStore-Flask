from flask import redirect, render_template, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from . import app
from . import controller

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

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/account/create')
def accountCreate():
    return render_template('account_create.html')