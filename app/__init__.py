from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)

'''# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress SQLAlchemy deprecation warnings

# Initialize SQLAlchemy extension
db = SQLAlchemy(app)'''

# Import routes and models (to avoid circular imports)
from app import routes, models