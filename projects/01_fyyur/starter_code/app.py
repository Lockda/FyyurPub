#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from datetime import date, datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

shows_table = db.Table('shows_table',
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
    db.Column('start_time', db.String(120), primary_key=True)
    )

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)
    artists = db.relationship('Artist', secondary= shows_table,
        backref=db.backref('venues', lazy=True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)

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
  return babel.dates.format_datetime(date, format)

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
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state).order_by('state').all()
  app.logger.info("areas ist: " + str(areas))
  
  data = []
  for area in areas:
    venues = Venue.query.filter_by(state=area.state).filter_by(city=area.city).order_by('name').all()
    venue_data =[]
    data.append({
    'city': area.city,
    'state': area.state,
    'venues': venue_data
    })
    for venue in venues:
      venue_data.append({
      'id': venue.id,
      'name': venue.name
      })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Implement search on venues with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # ----------------> DONE :)
  search_term = request.form.get('search_term', '')
  venues_name = Venue.query.filter(Venue.name.ilike("%{}%".format(search_term)))

  response={
    "count": venues_name.count(),
    "data": venues_name
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue = Venue.query.filter_by(id=venue_id).first()

  upcoming_shows_data = db.session.query(Artist, shows_table).join(shows_table).\
    filter(
        shows_table.c.venue_id == venue_id,
        shows_table.c.start_time >= str(datetime.now())
    ).all()

  past_shows_data = db.session.query(Artist, shows_table).join(shows_table).\
    filter(
        shows_table.c.venue_id == venue_id,
        shows_table.c.start_time < str(datetime.now())
    ).all()

  upcoming_shows = []
  for i in range(len(upcoming_shows_data)):
    upcoming_shows.append({
      'artist_id': upcoming_shows_data[i].Artist.id,
      'artist_name': upcoming_shows_data[i].Artist.name,
      'artist_image_link': upcoming_shows_data[i].Artist.image_link,
      'start_time': upcoming_shows_data[i].start_time
    })

  past_shows = []
  for i in range(len(past_shows_data)):
    past_shows.append({
      'artist_id': past_shows_data[i].Artist.id,
      'artist_name': past_shows_data[i].Artist.name,
      'artist_image_link': past_shows_data[i].Artist.image_link,
      'start_time': past_shows_data[i].start_time
    })
  
  app.logger.info("show_list = " + str(upcoming_shows))
  
  dataDic ={
     'id': venue.id,
     'name': venue.name,
     'city': venue.city,
     'state': venue.state,
     'phone': venue.phone,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
     'address': venue.address,
     'website': venue.website,
     'facebook_link': venue.facebook_link,
     'image_link': venue.image_link,
     'seeking_talent': venue.seeking_talent,
     'seeking_description': venue.seeking_description,
     'genres': [venue.genres],
     'upcoming_shows': upcoming_shows,
     'upcoming_shows_count': len(upcoming_shows),
     'past_shows': past_shows,
     'past_shows_count': len(past_shows)
    }
  
  return render_template('pages/show_venue.html', venue=dataDic)

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

  name = request.form.get('name', '')
  city = request.form.get('city', '')
  state = request.form.get('state', '')
  address = request.form.get('address', '')
  phone = request.form.get('phone', '')
  genres = request.form.getlist('genres')
  website = request.form.get('website', '')
  facebook_link = request.form.get('facebook_link', '')
  image_link = request.form.get('image_link', '')
  seeking_description = request.form.get('seeking_description', '')

  venue_add = Venue(name=name, city=city, state=state, address=address, 
  phone=phone, genres= genres, facebook_link=facebook_link, website=website, image_link=image_link, seeking_description=seeking_description)

  error = False

  try:
    db.session.add(venue_add)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')


  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  try:
   db.session.delete(id=venue_id)
   db.session.commit()
  except:
   db.session.rollback()
   print(sys.exc_info())
  finally:
   db.session.close()



  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = []
  artists = Artist.query.order_by('name').all()
  
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form.get('search_term', '')
  artists_name = Artist.query.filter(Artist.name.ilike("%{}%".format(search_term)))

  response={
    "count": artists_name.count(),
    "data": artists_name
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  artist = Artist.query.filter_by(id=artist_id).first()

  upcoming_shows_data = db.session.query(Venue, shows_table).join(shows_table).\
    filter(
        shows_table.c.artist_id == artist_id,
        shows_table.c.start_time >= str(datetime.now())
    ).all()

  past_shows_data = db.session.query(Venue, shows_table).join(shows_table).\
    filter(
        shows_table.c.artist_id == artist_id,
        shows_table.c.start_time < str(datetime.now())
    ).all()

  upcoming_shows = []
  for i in range(len(upcoming_shows_data)):
    upcoming_shows.append({
      'venue_id': upcoming_shows_data[i].Venue.id,
      'venue_name': upcoming_shows_data[i].Venue.name,
      'venue_image_link': upcoming_shows_data[i].Venue.image_link,
      'start_time': upcoming_shows_data[i].start_time
    })

  past_shows = []
  for i in range(len(past_shows_data)):
    past_shows.append({
      'venue_id': past_shows_data[i].Venue.id,
      'venue_name': past_shows_data[i].Venue.name,
      'venue_image_link': past_shows_data[i].Venue.image_link,
      'start_time': past_shows_data[i].start_time
    })

  
  dataDic ={
    'id': artist.id,
    'name': artist.name,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link,
    'image_link': artist.image_link,
    'seeking_description': artist.seeking_description,
    'genres': [artist.genres],
    'upcoming_shows': upcoming_shows,
    'upcoming_shows_count': len(upcoming_shows),
    'past_shows': past_shows,
    'past_shows_count': len(past_shows)
   }
    
  return render_template('pages/show_artist.html', artist=dataDic)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  name = request.form.get('name', '')
  city = request.form.get('city', '')
  state = request.form.get('state', '')
  address = request.form.get('address', '')
  phone = request.form.get('phone', '')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link', '')

  artist_to_update = Artist.query.filter_by(id=artist_id).first()
  artist_to_update.name = name
  artist_to_update.city = city
  artist_to_update.state = state
  artist_to_update.address = address
  artist_to_update.phone = phone
  artist_to_update.genres = genres
  artist_to_update.facebook_link = facebook_link

  db.session.commit()
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
 
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  form = VenueForm()

  name = request.form.get('name', '')
  city = request.form.get('city', '')
  state = request.form.get('state', '')
  address = request.form.get('address', '')
  phone = request.form.get('phone', '')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link', '')
  seeking_description = request.form.get('seeking_description', '')

  venue_to_update = Venue.query.filter_by(id=venue_id).first()
  venue_to_update.name = name
  venue_to_update.city = city
  venue_to_update.state = state
  venue_to_update.address = address
  venue_to_update.phone = phone
  venue_to_update.genres = genres
  venue_to_update.facebook_link = facebook_link
  venue_to_update.seeking_description = seeking_description
  venue_to_update.seeking_talent = form.seeking_talent.data

  db.session.commit()

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
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
    name = request.form.get('name', '') # e.g., flash('An error occurred. Show could not be listed.')
    state = request.form.get('state', '')
    phone = request.form.get('phone', '')
    genres = request.form.getlist('genres')
    website = request.form.get('website', '')
    facebook_link = request.form.get('facebook_link', '')
    image_link = request.form.get('image_link', '')

    artist_add = Artist(name=name, city=city, state=state, phone=phone, genres= genres, facebook_link=facebook_link, website=website, image_link=image_link)

    db.session.add(artist_add)
    db.session.commit()
  except:
    error = True
    flash('Error: Venue ' + name + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  
  if error == False:
    flash('Artist ' + name + ' was successfully listed!')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  datalist = []

  showdata = db.session.query(shows_table).all()

  for show in showdata:
    
    id_v = show.venue_id
    id_a = show.artist_id

    venue_name = db.session.query(Venue.name).filter_by(id=id_v).first()
    artist_name = db.session.query(Artist.name).filter_by(id=id_a).first()
    artist_image_link = db.session.query(Artist.image_link).filter_by(id=id_a).first()

    app.logger.info("simon, venue_id: " + str(artist_image_link))
    datalist.append({
      'venue_id': show.venue_id,
      'venue_name': venue_name[0],
      'artist_id': show.artist_id,
      'artist_name': artist_name[0],
      'artist_image_link': artist_image_link[0],
      'start_time': show.start_time
    })  

  return render_template('pages/shows.html', shows=datalist)

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
    venue_id = request.form.get('venue_id', '')
    artist_id = request.form.get('artist_id', '')
    date = request.form.get('start_time', '')

    show_add = shows_table.insert().values(venue_id=venue_id, artist_id=artist_id, start_time=date)
    db.session.execute(show_add)
    db.session.commit()
  except:
    error = True
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  
  if error == False:
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
