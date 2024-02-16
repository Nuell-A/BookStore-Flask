from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import config

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{config.sql_username}:{config.sql_pass}@localhost/{config.sql_db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress SQLAlchemy deprecation warnings

# Initialize SQLAlchemy extension
db = SQLAlchemy(app)
col = db.Column
string = db.String
integer = db.Integer

# Import routes and models (to avoid circular imports)
from app import routes, models, controller