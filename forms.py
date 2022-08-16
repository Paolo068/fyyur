import re
from datetime import datetime
from flask_wtf import Form
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    TelField,
)
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError


def validate_us_phone(form, phone):
    us_phone_num = "/^\\(?([0-9]{3})\\)?[-.\\s]?([0-9]{3})[-.\\s]?([0-9]{4})$/"
    match = re.search(us_phone_num, phone.data)
    if not match:
        raise ValidationError("Error, phone number must be in format xxx-xxx-xxxx")


def validate_fb_link(form, facebook_link):
    fb_url = "^(:http:\/\/?(?:www.)?facebook.com\/\w'"
    match = re.search(fb_url, facebook_link.data)
    if not match:
        raise ValidationError("Error, this is not a valid facebook url")


class ShowForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state",
        validators=[DataRequired()],
        choices=[
            ("AL", "AL"),
            ("AK", "AK"),
            ("AZ", "AZ"),
            ("AR", "AR"),
            ("CA", "CA"),
            ("CO", "CO"),
            ("CT", "CT"),
            ("DE", "DE"),
            ("DC", "DC"),
            ("FL", "FL"),
            ("GA", "GA"),
            ("HI", "HI"),
            ("ID", "ID"),
            ("IL", "IL"),
            ("IN", "IN"),
            ("IA", "IA"),
            ("KS", "KS"),
            ("KY", "KY"),
            ("LA", "LA"),
            ("ME", "ME"),
            ("MT", "MT"),
            ("NE", "NE"),
            ("NV", "NV"),
            ("NH", "NH"),
            ("NJ", "NJ"),
            ("NM", "NM"),
            ("NY", "NY"),
            ("NC", "NC"),
            ("ND", "ND"),
            ("OH", "OH"),
            ("OK", "OK"),
            ("OR", "OR"),
            ("MD", "MD"),
            ("MA", "MA"),
            ("MI", "MI"),
            ("MN", "MN"),
            ("MS", "MS"),
            ("MO", "MO"),
            ("PA", "PA"),
            ("RI", "RI"),
            ("SC", "SC"),
            ("SD", "SD"),
            ("TN", "TN"),
            ("TX", "TX"),
            ("UT", "UT"),
            ("VT", "VT"),
            ("VA", "VA"),
            ("WA", "WA"),
            ("WV", "WV"),
            ("WI", "WI"),
            ("WY", "WY"),
        ],
    )
    address = StringField("address", validators=[DataRequired()])
    phone = TelField(
        "phone", validators=[DataRequired(), validate_us_phone], default="(+1) "
    )
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        # TODO implement enum restriction
        "genres",
        validators=[DataRequired()],
        choices=[
            ("Alternative", "Alternative"),
            ("Blues", "Blues"),
            ("Classical", "Classical"),
            ("Country", "Country"),
            ("Electronic", "Electronic"),
            ("Folk", "Folk"),
            ("Funk", "Funk"),
            ("Hip-Hop", "Hip-Hop"),
            ("Heavy Metal", "Heavy Metal"),
            ("Instrumental", "Instrumental"),
            ("Jazz", "Jazz"),
            ("Musical Theatre", "Musical Theatre"),
            ("Pop", "Pop"),
            ("Punk", "Punk"),
            ("R&B", "R&B"),
            ("Reggae", "Reggae"),
            ("Rock n Roll", "Rock n Roll"),
            ("Soul", "Soul"),
            ("Other", "Other"),
        ],
    )
    facebook_link = StringField("facebook_link", validators=[URL(), validate_fb_link])
    website_link = StringField("website_link")

    seeking_talent = BooleanField("seeking_talent")

    seeking_description = StringField("seeking_description")


class ArtistForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state",
        validators=[DataRequired()],
        choices=[
            ("AL", "AL"),
            ("AK", "AK"),
            ("AZ", "AZ"),
            ("AR", "AR"),
            ("CA", "CA"),
            ("CO", "CO"),
            ("CT", "CT"),
            ("DE", "DE"),
            ("DC", "DC"),
            ("FL", "FL"),
            ("GA", "GA"),
            ("HI", "HI"),
            ("ID", "ID"),
            ("IL", "IL"),
            ("IN", "IN"),
            ("IA", "IA"),
            ("KS", "KS"),
            ("KY", "KY"),
            ("LA", "LA"),
            ("ME", "ME"),
            ("MT", "MT"),
            ("NE", "NE"),
            ("NV", "NV"),
            ("NH", "NH"),
            ("NJ", "NJ"),
            ("NM", "NM"),
            ("NY", "NY"),
            ("NC", "NC"),
            ("ND", "ND"),
            ("OH", "OH"),
            ("OK", "OK"),
            ("OR", "OR"),
            ("MD", "MD"),
            ("MA", "MA"),
            ("MI", "MI"),
            ("MN", "MN"),
            ("MS", "MS"),
            ("MO", "MO"),
            ("PA", "PA"),
            ("RI", "RI"),
            ("SC", "SC"),
            ("SD", "SD"),
            ("TN", "TN"),
            ("TX", "TX"),
            ("UT", "UT"),
            ("VT", "VT"),
            ("VA", "VA"),
            ("WA", "WA"),
            ("WV", "WV"),
            ("WI", "WI"),
            ("WY", "WY"),
        ],
    )
    phone = TelField(
        "phone", validators=[DataRequired(), validate_us_phone], default="(+1) "
    )
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=[
            ("Alternative", "Alternative"),
            ("Blues", "Blues"),
            ("Classical", "Classical"),
            ("Country", "Country"),
            ("Electronic", "Electronic"),
            ("Folk", "Folk"),
            ("Funk", "Funk"),
            ("Hip-Hop", "Hip-Hop"),
            ("Heavy Metal", "Heavy Metal"),
            ("Instrumental", "Instrumental"),
            ("Jazz", "Jazz"),
            ("Musical Theatre", "Musical Theatre"),
            ("Pop", "Pop"),
            ("Punk", "Punk"),
            ("R&B", "R&B"),
            ("Reggae", "Reggae"),
            ("Rock n Roll", "Rock n Roll"),
            ("Soul", "Soul"),
            ("Other", "Other"),
        ],
    )
    facebook_link = StringField("facebook_link", validators=[URL(), validate_fb_link])

    website_link = StringField("website_link")

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description")
