#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (Flask, render_template, request, Response, flash, redirect, url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import update
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
import array
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
#Done!!
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String)
    venue_shows = db.relationship('Show', backref=db.backref('venue'))
def __str__(self):
  return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # Done!!
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
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
def __str__(self):
  return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # Done!!
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# Artist is already implemented
class Show(db.Model):
  __tablename__ = 'show'
  
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
  start_time = db.Column(db.DateTime, default = datetime.now)


class Show_view:
  def __init__(self, venue_id, venue_name, artist_id, artist_name, artist_image_link, start_time):
    self.venue_id= venue_id
    self.venue_name= venue_name
    self.artist_id= artist_id   
    self.artist_name= artist_name
    self.artist_image_link= artist_image_link
    self.start_time= start_time
  def __str__(self):
     return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

class Show_venue_dto:
  def __init__(self, id, name, genres, address, city, state, phone, website, facebook_link, seeking_talent, seeking_description, image_link, past_shows, upcoming_shows, past_shows_count, upcoming_shows_count):
    self.id= id
    self.name = name
    self.genres = genres
    self.address = address
    self.city = city
    self.state = state
    self.phone = phone
    self.website = website
    self.facebook_link =facebook_link
    self.seeking_talent = seeking_talent
    self.seeking_description = seeking_description
    self.image_link = image_link
    self.past_shows = past_shows
    self.upcoming_shows = upcoming_shows
    self.past_shows_count = past_shows_count
    self.upcoming_shows_count = upcoming_shows_count
  def __str__(self):
    return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

class Show_Artist_dto:
  def __init__(self, id, name, genres, city, state, phone, website, facebook_link, seeking_venue, seeking_description, image_link, past_shows, upcoming_shows, past_shows_count, upcoming_shows_count):
    self.id= id
    self.name = name
    self.genres = genres
    self.city = city
    self.state = state
    self.phone = phone
    self.website = website
    self.facebook_link =facebook_link
    self.seeking_venue = seeking_venue
    self.seeking_description = seeking_description
    self.image_link = image_link
    self.past_shows = past_shows
    self.upcoming_shows = upcoming_shows
    self.past_shows_count = past_shows_count
    self.upcoming_shows_count = upcoming_shows_count
class Venue_list_dto:
  def __init__(self, id, name, num_upcoming_shows):
    self.id= id
    self.name= name
    self.num_upcoming_shows=num_upcoming_shows
class Show_venue_list_dto:
  def __init__(self, city, state, venues):
    self.city = city
    self.state = state
    self.venues = venues
class area_dto:
  def __init__(self,city, state):
    self.city = city
    self.state = state
  def __str__(self):
    return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
class search_venue:
  def __init__(self, count, data):
    self.count= count
    self.data= data
  def __str__(self):
    return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
class search_data:
  def __init__(self, id, name, num_upcoming_shows):
    self.id = id
    self.name = name
    self.num_upcoming_shows = num_upcoming_shows
  def __str__(self):
    return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
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
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data =[]
  venues = Venue.query.all()
  venue_list=[]
  areas=[]
# prepare the areas
  for venue in venues:
    venue.city
    area= area_dto(venue.city,venue.state)
    areas.append(area)

# Step prepare the venues 
  for venue in venues:
    upcoming_shows= []
    past_shows=[]
    venue_shows= Show.query.filter_by(venue_id = venue.id).all()
    for venue_show in venue_shows:
      artist = Artist.query.filter_by(id = venue_show.artist_id).first()
      show = Show_view(venue_show.venue_id,venue.name,venue_show.artist_id,artist.name,artist.image_link,str(venue_show.start_time))
      if str(show.start_time) < str(datetime.now):   
        past_shows.append(show)
      else:
        upcoming_shows.append(show)
    venue_view =Show_venue_dto(venue.id,
      venue.name,
      venue.genres,
      venue.address,
      venue.city,
      venue.state,
      venue.phone,
      venue.website,
      venue.facebook_link,
      venue.seeking_talent,
      venue.seeking_description,
      venue.image_link,
      past_shows,
      upcoming_shows,
      len(past_shows),
      len(upcoming_shows)
      )
    venue_list.append(venue_view)

# step build list of venues based on area
  for area in areas:
    area_venues=[]
    for venue in venue_list:
      if venue.city == area.city and venue.state == area.state:
        area_venues.append(venue)
    data.append(Show_venue_list_dto(area.city,area.state,area_venues))  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search=request.form.get('search_term')
  venue_list = Venue.query.filter(Venue.name.ilike(f'%{search}%'))

  data_list=[]
  for venue in venue_list:
    venue_shows = Show.query.filter_by(venue_id = venue.id)
    upcoming_shows= []
    for venue_show in venue_shows:
      artist = Artist.query.filter_by(id = venue_show.artist_id).first()
      show = Show_view(venue_show.venue_id,venue.name,venue_show.artist_id,artist.name,artist.image_link,str(venue_show.start_time))
      if str(show.start_time) > str(datetime.now):   
        upcoming_shows.append(show)
    data=search_data(venue.id, venue.name,len(upcoming_shows))
    data_list.append(data)
  respose = search_venue(len(data_list),data_list)
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=respose, search_term=request.form.get('search_term'))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue = Venue.query.get(venue_id)
  venue_shows = Show.query.filter_by(venue_id = venue_id)
  past_shows=[]
  upcoming_shows=[]
  
  for venue_show in venue_shows:
    artist = Artist.query.filter_by(id = venue_show.artist_id).first()
    show = Show_view(venue_show.venue_id,venue.name,venue_show.artist_id,artist.name,artist.image_link,str(venue_show.start_time))
    if str(show.start_time) < str(datetime.now):   
      past_shows.append(show)
    else:
      upcoming_shows.append(show)
  data =Show_venue_dto(venue_id,
    venue.name,
    venue.genres,
    venue.address,
    venue.city,
    venue.state,
    venue.phone,
    venue.website,
    venue.facebook_link,
    venue.seeking_talent,
    venue.seeking_description,
    venue.image_link,
    past_shows,
    upcoming_shows,
    len(past_shows),
    len(upcoming_shows)
  )
  return render_template('pages/show_venue.html', venue=data)

  # 
  # ],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  # return render_template('pages/show_venue.html', venue=data)
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
  venueForm = VenueForm(request.form, csrf_enabled=False)
  venue = Venue()
  if venueForm.validate_on_submit():
    try:
      venue.name = venueForm.name.data
      venue.city =  venueForm.city.data
      venue.state=  venueForm.state.data
      venue.address= venueForm.address.data
      venue.phone=  venueForm.phone.data
      venue.genres=  venueForm.genres.data
      venue.facebook_link= venueForm.facebook_link.data
      venue.image_link= venueForm.image_link.data
      venue.website=  venueForm.website.data
      if request.form.get('seeking_talent') == 'True' :   
        venue.seeking_talent= True 
      else:
        venue.seeking_talent= False
      venue.seeking_description= request.form.get('seeking_description')

      db.session.add(venue)
      db.session.commit()

        # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('Venue ' + request.form['name'] + ' cannot be listed')
    finally:
      db.session.close()

    # TODO: modify data to be the data object returned from db insertion
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    
    return render_template('pages/home.html')
  return render_template('forms/new_venue.html',form= venueForm)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
    venue_shows_list= Show.query.filter_by(venue_id=venue_id).all()
    for venue_show in venue_shows_list:
      venue_show.first().delete()
    venue_deleted= Venue.query.filter_by(venue_id=venue_id)
    venue_deleted.first().delete()
    db.session.commit()
    flash('Venue ' + venue_id + ' was successfully Deleted!')
  except:
    db.session.rollback()
    flash('Venue ' + venue_id + ' is not Deleted!')
  finally:
    db.session.close()
  return render_template('pages/home.html')
  # return None
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()

  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search=request.form.get('search_term')
  artist_list = Artist.query.filter(Artist.name.ilike(f'%{search}%'))

  data_list=[]
  
  for artist in artist_list:
    artist_shows = Show.query.filter_by(artist_id = artist.id)
    upcoming_shows= []
    for artist_show in artist_shows:
      venue = Venue.query.filter_by(id = artist_show.venue_id).first()
      show = Show_view(artist_show.venue_id,venue.name,artist_show.artist_id,artist.name,artist.image_link,str(artist_show.start_time))
      if str(show.start_time) > str(datetime.now):   
        upcoming_shows.append(show)
    data=search_data(venue.id, venue.name,len(upcoming_shows))
    data_list.append(data)
  respose = search_venue(len(data_list),data_list)


  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  artist = Artist.query.get(artist_id)
  artist_shows = Show.query.filter_by(artist_id = artist_id)
  past_shows=[]
  upcoming_shows=[]
  for artist_show in artist_shows:
    venue = Venue.query.filter_by(id =  artist_show.venue_id).first()
    show = Show_view(artist_show.venue_id,venue.name,artist_show.artist_id,artist.name,artist.image_link,str(artist_show.start_time))
    if str(show.start_time) < str(datetime.now):   
      past_shows.append(show)
    else:
      upcoming_shows.append(show)
     
  artist_data =Show_Artist_dto(artist.id,
      artist.name,
      artist.genres,
      artist.city,
      artist.state,
      artist.phone,
      artist.website,
      artist.facebook_link,
      artist.seeking_venue,
      artist.seeking_description,
      artist.image_link,
      past_shows,
      upcoming_shows,
      len(past_shows),
      len(upcoming_shows)
  )
  return render_template('pages/show_artist.html', artist=artist_data)

  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  # return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET','POST'])
def edit_artist(artist_id):
  if request.method =="POST":
    form = ArtistForm(request.form, csrf_enabled=False)
    artist=Artist()
    if form.validate_on_submit():
      try:
          artist.name = form.name.data
          artist.city =  form.city.data
          artist.state=  form.state.data
          artist.phone=  form.phone.data
          artist.genres=  form.genres.data
          artist.facebook_link= form.facebook_link.data
          artist.image_link= form.image_link.data
          artist.website=  form.website.data 
          if request.form.get('seeking_talent') == 'True' :   
            artist.seeking_venue= True 
          else:
            artist.seeking_venue= False
            artist.seeking_description = form.seeking_description.data
          db.session.add(artist)
          db.session.commit()
          # on successful db insert, flash success
          flash('artist ' + request.form['name'] + ' updated successfully!')
      except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' + request.form['name'] +' could not be updated.')
        return render_template('forms/edit_artist.html', form=form, artist=artist)
      finally:
        db.session.close()
    # TODO: populate form with fields from artist with ID <artist_id>
    
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      return render_template('pages/home.html')
  # return render_template('forms/new_artist.html', form=form)
  else:
    artist = Artist.query.filter_by(id=artist_id).first()
    form = ArtistForm(obj=artist) 
    return render_template('forms/edit_artist.html',form=form,artist=artist)
    

# @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
# def edit_artist_submission(artist_id):
#   # TODO: take values from the form submitted, and update existing
#   # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  form = VenueForm(obj=venue)
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venueForm = VenueForm(request.form, csrf_enabled=False)
  venue = Venue.query.filter_by(id=venue_id).first()
  print(venueForm.validate_on_submit())
  if venueForm.validate_on_submit():
    try:
      venue.name = venueForm.name.data
      venue.city =  venueForm.city.data
      venue.state=  venueForm.state.data
      venue.address= venueForm.address.data
      venue.phone=  venueForm.phone.data
      venue.genres=  venueForm.genres.data
      venue.facebook_link= venueForm.facebook_link.data
      venue.image_link= venueForm.image_link.data
      venue.website=  venueForm.website.data
      if request.form.get('seeking_talent') == 'True' :   
        venue.seeking_talent= True 
      else:
        venue.seeking_talent= False
      venue.seeking_description= request.form.get('seeking_description')
      db.session.commit()

        # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully Updated!')
      return redirect(url_for('show_venue', venue_id=venue_id))
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('Venue ' + request.form['name'] + ' cannot be listed')
      return render_template('forms/edit_venue.html', form=venueForm, venue=venue)
    finally:
      db.session.close()

    # TODO: modify data to be the data object returned from db insertion
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    
    return render_template('pages/home.html')
  return render_template('forms/edit_venue.html', form=venueForm, venue=venue)

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
  print(request.form)
  artistForm=ArtistForm(request.form, csrf_enabled=False)
  artist = Artist()
  show = Show()
  if artistForm.validate_on_submit():
    try:

      artist.name = artistForm.name.data
      artist.city =  artistForm.city.data
      artist.state=  artistForm.state.data
      artist.phone=  artistForm.phone.data
      artist.genres=  artistForm.genres.data
      artist.facebook_link= artistForm.facebook_link.data
      artist.image_link= artistForm.image_link.data
      artist.website=  artistForm.website.data
      if request.form.get('seeking_venue') == 'True' :   
        artist.seeking_venue= True 
      else:
        artist.seeking_venue= False
      artist.seeking_description= artistForm.seeking_description.data
      db.session.add(artist)
      db.session.commit()

        # on successful db insert, flash success
      flash('artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    finally:
      db.session.close()
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
  return render_template('forms/new_artist.html', form=artistForm)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data=[]
  for dbshow in shows:
    venue = Venue.query.filter_by(id = dbshow.venue_id).first()
    artist = Artist.query.filter_by(id = dbshow.artist_id).first()
    
    show = Show_view(dbshow.venue_id,venue.name,dbshow.artist_id,artist.name,artist.image_link,str(dbshow.start_time))
    data.append(show)

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
  showForm = ShowForm(request.form, csrf_enabled=False)
  show = Show()
  if showForm.validate_on_submit():
    try:
      show.venue_id = showForm.venue_id.data
      show.artist_id =  showForm.artist_id.data
      show.start_time=  showForm.start_time.data
      db.session.add(show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
 

    # on successful db insert, flash success
    # flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')
    
  return render_template('forms/new_show.html', form=showForm)

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
