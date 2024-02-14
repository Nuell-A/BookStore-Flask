from flask import redirect, render_template, request
from . import app
# Import models

@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    search_results = ["Lion King", "Spirit of the Stallion", "Suuuppppperrrrr long name for testing purposes"]
    context = {
        "search": search,
        "search_results": search_results
    }
    return render_template('home.html', context=context)