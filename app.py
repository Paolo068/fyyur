# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from time import strptime
from config import *
from models import *
from sqlalchemy import or_
from email.policy import default
import json
import sys
from unittest import result
import babel
import logging
from dateutil.parser import parse
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

# ----------------------------------------------------------------------------#
# App Config => config.py
# ----------------------------------------------------------------------------#


# ----------------------------------------------------------------------------#
# Models => models.py
# ----------------------------------------------------------------------------#


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  ----------------------------------------------------------------
#  VENUES
#  ----------------------------------------------------------------
@app.route("/venues")
def venues():
    return render_template("pages/venues.html", venues=Venue.query.all())


# Create_venue
# ----------------------------------------------------------------
@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm()

    name = form.name.data.strip()
    city = form.city.data.strip()
    state = form.state.data
    address = form.address.data.strip()
    phone = form.phone.data.strip()
    genres = form.genres.data
    facebook_link = form.facebook_link.data.strip()
    image_link = form.image_link.data
    website_link = form.website_link.data.strip()
    seeking_talent = True if "seeking_talent" in request.form else False
    seeking_description = form.seeking_description.data.strip()

    if not form.validate_on_submit():
        flash(form.errors)
        return redirect(url_for("create_artist_submission"))
    else:
        try:
            new_venue = Venue(
                name=name,
                city=city,
                state=state,
                address=address,
                phone=phone,
                genres=genres,
                facebook_link=facebook_link,
                image_link=image_link,
                website_link=website_link,
                seeking_talent=seeking_talent,
                seeking_description=seeking_description,
            )
            db.session.add(new_venue)
            db.session.commit()
            flash("Venue " + request.form["name"] + " was successfully listed!")

        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                "An error occurred. Venue "
                + request.form["name"]
                + " could not be listed.!"
            )

        finally:
            db.session.close()
        return render_template("pages/home.html")


# Show_venue_details
# ----------------------------------------------------------------
@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    current_time = format_datetime(str(datetime.utcnow()))

    upcoming_shows = Show.query.filter(
        Show.venue_id == venue_id, Show.start_time >= current_time
    ).all()

    past_shows = Show.query.filter(
        Show.venue_id == venue_id, Show.start_time < current_time
    ).all()

    return render_template(
        "pages/show_venue.html",
        venue=venue,
        upcoming_shows=upcoming_shows,
        past_shows=past_shows,
    )


# Update_venue
# ----------------------------------------------------------------
@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):

    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)

    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    form = VenueForm()

    name = form.name.data.strip()
    city = form.city.data.strip()
    state = form.state.data
    address = form.address.data.strip()
    phone = form.phone.data.strip()
    genres = form.genres.data
    facebook_link = form.facebook_link.data.strip()
    image_link = form.image_link.data
    website_link = form.website_link.data.strip()
    seeking_talent = True if "seeking_talent" in request.form else False
    seeking_description = form.seeking_description.data.strip()

    if not form.validate():
        flash(form.errors)
        return redirect(url_for("edit_venue_submission", venue_id=venue_id))

    else:
        try:
            venue = Venue.query.get_or_404(venue_id)

            venue.name = name
            venue.city = city
            venue.state = state
            venue.address = address
            venue.phone = phone
            venue.genres = genres
            venue.facebook_link = facebook_link
            venue.image_link = image_link
            venue.website_link = website_link
            venue.seeking_talent = seeking_talent
            venue.seeking_description = seeking_description

            db.session.commit()
            flash('Venue "' + request.form["name"] + '" was successfully updated!')
            return redirect(url_for("show_venue", venue_id=venue.id))

        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                'An error occurred. Venue "'
                + request.form["name"]
                + '" could not be updated!'
            )

        finally:
            db.session.close()
            return redirect(url_for("index"))


# Delete_venue
# ----------------------------------------------------------------
@app.route("/venues/<int:venue_id>/delete", methods=["GET"])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get_or_404(venue_id)
        db.session.delete(venue)

        db.session.commit()
        flash("Venue was successfully deleted!")
        return redirect(url_for("index"))

    except:
        db.session.rollback()
        print(sys.exc_info())
        flash("Venue " + request.form["name"] + " could not be deleted!")

    finally:
        db.session.close()
    return redirect(url_for("index"))


# Search_venue
# ----------------------------------------------------------------
@app.route("/venues/search", methods=["POST"])
def search_venues():
    search_term = request.form.get("search_term")
    search_results = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()
    return render_template(
        "pages/search_venues.html",
        search_term=request.form.get("search_term", ""),
        results=search_results,
    )


#  ----------------------------------------------------------------
#  ARTISTS
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    return render_template("pages/artists.html", artists=Artist.query.all())


# Create_artist
# ----------------------------------------------------------------
@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    form = ArtistForm()

    name = form.name.data.strip()
    city = form.city.data.strip()
    state = form.state.data
    phone = form.phone.data.strip()
    genres = form.genres.data
    facebook_link = form.facebook_link.data.strip()
    image_link = form.image_link.data
    website_link = form.website_link.data.strip()
    seeking_venue = True if "seeking_venue" in request.form else False
    seeking_description = form.seeking_description.data.strip()

    if not form.validate_on_submit():
        flash(form.errors)
        return redirect(url_for("create_artist_submission"))
    else:
        try:
            new_artist = Artist(
                name=name,
                city=city,
                state=state,
                phone=phone,
                genres=genres,
                facebook_link=facebook_link,
                image_link=image_link,
                website_link=website_link,
                seeking_venue=seeking_venue,
                seeking_description=seeking_description,
            )
            db.session.add(new_artist)
            db.session.commit()
            flash("Artist " + request.form["name"] + " was successfully listed!")

        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                "An error occurred. Artist "
                + request.form["name"]
                + " could not be listed.!"
            )

        finally:
            db.session.close()
        return render_template("pages/home.html")


# Show_artist_details
# ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    current_time = format_datetime(str(datetime.utcnow()))

    upcoming_shows = Show.query.filter(
        Show.artist_id == artist_id, Show.start_time >= current_time
    ).all()

    past_shows = Show.query.filter(
        Show.artist_id == artist_id, Show.start_time < current_time
    ).all()

    return render_template(
        "pages/show_artist.html",
        artist=artist,
        upcoming_shows=upcoming_shows,
        past_shows=past_shows,
    )


# Update_artist
# ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm()

    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form = ArtistForm()

    name = form.name.data.strip()
    city = form.city.data.strip()
    state = form.state.data
    phone = form.phone.data.strip()
    genres = form.genres.data
    facebook_link = form.facebook_link.data.strip()
    image_link = form.image_link.data
    website_link = form.website_link.data.strip()
    seeking_venue = True if "seeking_venue" in request.form else False
    seeking_description = form.seeking_description.data.strip()

    if not form.validate():
        flash(form.errors)
        return redirect(url_for("edit_artist_submission", artist_id=artist_id))

    else:
        try:
            artist = Artist.query.get_or_404(artist_id)

            artist.name = name
            artist.city = city
            artist.state = state
            artist.phone = phone
            artist.genres = genres
            artist.facebook_link = facebook_link
            artist.image_link = image_link
            artist.website_link = website_link
            artist.seeking_venue = seeking_venue
            artist.seeking_description = seeking_description

            db.session.commit()
            flash('Artist "' + request.form["name"] + '" was successfully updated!')

        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                'An error occurred. Artist "'
                + request.form["name"]
                + '" could not be updated.!'
            )

        finally:
            db.session.close()
        return redirect(url_for("index"))


# Delete_artist
# ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/delete", methods=["GET"])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get_or_404(artist_id)

        db.session.delete(artist)
        db.session.commit()
        flash("Artist was successfully deleted!")
        return redirect(url_for("index"))

    except:
        db.session.rollback()
        print(sys.exc_info())
        flash("Artist " + request.form["name"] + " could not be deleted!")

    finally:
        db.session.close()
    return redirect(url_for("index"))


# Search_artist
# ----------------------------------------------------------------
@app.route("/artists/search", methods=["POST"])
def search_artists():
    try:
        search_term = request.form.get("search_term")
        search_results = Artist.query.filter(
            Artist.name.ilike("%" + search_term + "%")
        ).all()
        return render_template(
            "pages/search_artists.html",
            search_term=request.form.get("search_term"),
            results=search_results,
        )

    except:
        db.session.rollback()


#  ----------------------------------------------------------------
#  SHOWS
#  ----------------------------------------------------------------
@app.route("/shows")
def shows():
    shows = Show.query.all()
    return render_template("pages/shows.html", shows=shows)


# Create_show
# ----------------------------------------------------------------
@app.route("/shows/create", methods=["GET"])
def create_shows():
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    try:
        artist_id = request.form["artist_id"]
        venue_id = request.form["venue_id"]
        start_time = format_datetime(request.form["start_time"])

        new_show = Show(
            artist_id=artist_id,
            venue_id=venue_id,
            start_time=start_time,
        )

        db.session.add(new_show)
        db.session.commit()

        flash("The show was successfully listed!")
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash("An error occured. The show could not be listed!")

    finally:
        db.session.close()
    return render_template("pages/home.html")


# Search_show
# ----------------------------------------------------------------
@app.route("/shows/search", methods=["POST"])
def search_shows():
    try:
        search_term = request.form.get("search_term")
        results = Show.query.where(
            or_(
                Show.venue_name.ilike("%" + search_term + "%"),
                Show.artist_name.ilike("%" + search_term + "%"),
            )
        ).all()
        return render_template(
            "pages/search_shows.html",
            search_term=request.form.get("search_term"),
            search_results=results,
        )

    except:
        db.session.rollback()


# -----------------------------------------------------------------#
#  UTILITIES
# -----------------------------------------------------------------#
@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
