from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import config


try:
    # Initialize Flask application
    print("Initializing Flask application.")
    app = Flask(__name__)
    app.secret_key = config.app_secret_key

    print("Connecting to database.")
    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{config.sql_username}:{config.sql_pass}@{config.sql_server}/book_store'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress SQLAlchemy deprecation warnings

    # Initialize SQLAlchemy extension
    db = SQLAlchemy(app)
    print("Initialization complete...")
except:
    print("There was an error during initialization...")



# Import routes and models (to avoid circular imports)
from app import routes, models, controller