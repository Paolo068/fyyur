from config import db
from sqlalchemy import ARRAY, String, Integer


class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(150))
    genres = db.Column(ARRAY(String))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(150))
    # artist = db.relationship("Artist", secondary="shows", backref="artists")


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(ARRAY(String))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(150))
    venues = db.relationship("Venue", secondary="shows", backref="artists")


class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    artist_name = db.Column(db.String(120))
    artist_image_link = db.Column(db.String(150))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"))
    venue_name = db.Column(db.String(120))
    start_time = db.Column(db.String(120))
    upcoming_shows = db.Column(ARRAY(Integer))
    past_shows = db.Column(ARRAY(Integer))
