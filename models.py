from distutils.ccompiler import show_compilers
from distutils.command.bdist import show_formats
from config import db
from sqlalchemy import ARRAY, String, Integer


class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(150))
    genres = db.Column(ARRAY(String))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(150))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(150))
    shows = db.relationship("Show", backref="venues", lazy=True)


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(ARRAY(String))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(150))
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(150))
    shows = db.relationship("Show", backref="artists", lazy=True)


class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"))
    start_time = db.Column(db.String())
