#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import traceback
import dateutil.parser
import babel
from flask_migrate import Migrate
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
SQLALCHEMY_DATABASE_URI ='postgresql://postgres:1111@localhost:5433/fyyur'

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Show(db.Model):
        __tablename__='Show'
        
        venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True, nullable=False)
        artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True, nullable=False)
        start_time = db.Column(db.DateTime, nullable=False)
class Venue(db.Model):
    __tablename__ = 'Venue'

    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean , default=False, nullable=False)
    seeking_describtion = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref = db.backref('venue', lazy=True))
    
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String , unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean , default=False, nullable=False)
    seeking_describtion = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref = db.backref('artist', lazy=True))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.    
    

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.

  #num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  venues = Venue.query.group_by(Venue.id,Venue.state,Venue.city).all()
  venue_city_state = ''
  i = 0
  for venue in venues:
    
    if venue_city_state != venue.city + ',' + venue.state:
      venue_city_state = venue.city + ',' + venue.state
      num_shows = Show.query.filter_by(venue_id=venue.id).count()
      
      record = {
      "city": venue.city,
      "state": venue.state,
      "venues": [{
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": num_shows,
      }]
    }
      data.insert(i, record)
      
      i=i+1
      
    else:
      record["venues"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": num_shows,
      })
    

  return render_template('pages/venues.html', areas=data)
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search = request.form.get('search_term','')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search}%')).all()
  count = Venue.query.filter(Venue.name.ilike(f'%{search}%')).count()
  
  data=[]
  i = 0
  for venue in venues:
        
    num_shows = Show.query.filter_by(venue_id=venue.id).count()
    
    record = {
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": num_shows,
    }
    data.insert(i, record)
    
    i=i+1

  response={
    "count": count,
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
  

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  shows = Show.query.filter_by(venue_id=venue_id).all()
  past_shows = []
  upcoming_shows = []
  now = datetime.now()
  i=0
  j=0
  for show in shows:
    artist = db.session.query(Artist).join(Show).filter_by(artist_id=show.artist_id).first()
    date_time = show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    record={
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": date_time
    }
    if(show.start_time>now):
      upcoming_shows.insert(i, record)
      i=i+1
    if(show.start_time<now):
      past_shows.insert(j, record)  
      j=j+1
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": j,
    "upcoming_shows_count": i,
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking_talent = request.form.get('seeking_talent') == 'True'
    seeking_describtion = request.form.get('seeking_describtion')

    
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, website=website, seeking_talent=seeking_talent, seeking_describtion=seeking_describtion)
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.

  except:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    db.session.rollback()
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  finally:
    db.session.close()

  return render_template('pages/home.html')

  
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
      
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  artists = Artist.query.all()
  i = 0
  for artist in artists:
    record =  {
    "id": artist.id,
    "name": artist.name,
  }
    data.insert(i, record)
    i=i+1

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search = request.form.get('search_term','')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search}%')).all()
  count = Artist.query.filter(Artist.name.ilike(f'%{search}%')).count()
  data=[]
  i = 0
  for artist in artists:
    num_shows = Show.query.filter_by(artist_id=artist.id).count()
    record = {
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_shows,
    }
    data.insert(i, record)
    i=i+1

  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  artist = Artist.query.filter_by(id=artist_id).first()
  shows = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
  upcoming_shows = []
  now = datetime.now()
  i=0
  j=0
  for show in shows:
    venue = db.session.query(Venue).join(Show).filter_by(venue_id=show.venue_id).first()
    date_time = show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    record={
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": date_time
    }
    if(show.start_time>now):
      upcoming_shows.insert(i, record)
      i=i+1
    if(show.start_time<now):
      past_shows.insert(j, record)  
      j=j+1

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "seeking_venue": artist.seeking_talent,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": j,
    "upcoming_shows_count": i,
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artistRecord = Artist.query.get(artist_id)
  
  artist={
    
    "id": artistRecord.id,
    "name": artistRecord.name,
    "genres": artistRecord.genres,
    "city": artistRecord.city,
    "state": artistRecord.state,
    "phone": artistRecord.phone,
    "website": artistRecord.website,
    "facebook_link": artistRecord.facebook_link,
    "seeking_venue": artistRecord.seeking_talent,
    "seeking_description": artistRecord.seeking_describtion,
    "image_link": artistRecord.image_link
    
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  artist = Artist.query.get(artist_id)
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking_talent = request.form.get('seeking_talent') == 'True'
    seeking_describtion = request.form.get('seeking_describtion')

    artist.name = name
    artist.city = city
    artist.state = state
    artist.phone = phone
    artist.image_link = image_link
    artist.genres = genres
    artist.facebook_link = facebook_link
    artist.website = website
    artist.seeking_talent = seeking_talent
    artist.seeking_describtion = seeking_describtion

    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')

  finally:
    db.session.close()
    
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venueRecord = Venue.query.get(venue_id)
  venue={
    "id": venueRecord.id,
    "name": venueRecord.name,
    "genres": venueRecord.genres,
    "address": venueRecord.address,
    "city": venueRecord.city,
    "state": venueRecord.state,
    "phone": venueRecord.phone,
    "website": venueRecord.website,
    "facebook_link": venueRecord.facebook_link,
    "seeking_talent": venueRecord.seeking_talent,
    "seeking_description": venueRecord.seeking_describtion,
    "image_link": venueRecord.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  venue = Venue.query.get(venue_id)
  
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking_talent = request.form.get('seeking_talent') == 'True'
    seeking_describtion = request.form.get('seeking_describtion')

    venue.name = name
    venue.city = city
    venue.state = state
    venue.address = address
    venue.phone = phone
    venue.image_link = image_link
    venue.genres = genres
    venue.facebook_link = facebook_link
    venue.website = website
    venue.seeking_talent = seeking_talent
    venue.seeking_describtion = seeking_describtion

    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')

  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')

  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking_talent = request.form.get('seeking_talent') == 'True'
    seeking_describtion = request.form.get('seeking_describtion')

    artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, website=website, seeking_talent=seeking_talent, seeking_describtion=seeking_describtion)
    db.session.add(artist)
    db.session.commit()

  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # except:
    # flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    # db.session.rollback()
    
  except Exception as err:
    print(traceback.format_exc())
    # or
    print(sys.exc_info()[2])
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  
  finally:
    db.session.close()
    
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data=[]
  i = 0
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    date_time = show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    record =  {
    "venue_id": venue.id,
    "venue_name": venue.name,
    "artist_id": artist.id,
    "artist_name": artist.name,
    "artist_image_link": artist.image_link,
    "start_time": date_time
  }
    data.insert(i, record)
    i=i+1
  
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    venue_id = request.form.get('venue_id')
    artist_id = request.form.get('artist_id')
    start_time = request.form.get('start_time')
    show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()

  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.debug = True
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''