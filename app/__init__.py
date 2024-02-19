from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import config


# Initialize Flask application
app = Flask(__name__)
app.secret_key = config.app_secret_key

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{config.sql_username}:{config.sql_pass}@localhost/{config.sql_db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress SQLAlchemy deprecation warnings

# Initialize SQLAlchemy extension
db = SQLAlchemy(app)

# Import routes and models (to avoid circular imports)
from app import routes, models, controller