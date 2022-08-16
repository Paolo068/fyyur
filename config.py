import os
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate


SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:admin@localhost:5432/fyyur"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
