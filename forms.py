from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL, Length, Regexp
from enum import Enum

#----------------------------------------------------------------------------#
# Enums.
#----------------------------------------------------------------------------#

class genres(Enum):
            Alternative = 'Alternative'
            Blues= 'Blues'
            Classical= 'Classical'
            Country= 'Country'
            Electronic= 'Electronic'
            Folk= 'Folk'
            Funk= 'Funk'
            HipHop= 'Hip-Hop'
            HeavyMetal= 'Heavy Metal'
            Instrumental= 'Instrumental'
            Jazz= 'Jazz'
            MusicalTheatre= 'Musical Theatre'
            Pop= 'Pop'
            Punk= 'Punk'
            RandB= 'R&B'
            Reggae= 'Reggae'
            RocknRoll= 'Rock n Roll'
            Soul= 'Soul'
            Other= 'Other'

class State(Enum):
            AL= 'AL'
            AK= 'AK'
            AZ= 'AZ'
            AR= 'AR'
            CA= 'CA'
            CO= 'CO'
            CT= 'CT'
            DE= 'DE'
            DC= 'DC'
            FL= 'FL'
            GA= 'GA'
            HI= 'HI'
            ID= 'ID'
            IL= 'IL'
            IN= 'IN'
            IA= 'IA'
            KS= 'KS'
            KY= 'KY'
            LA= 'LA'
            ME= 'ME'
            MT= 'MT'
            NE= 'NE'
            NV= 'NV'
            NH= 'NH'
            NJ= 'NJ'
            NM= 'NM'
            NY= 'NY'
            NC= 'NC'
            ND= 'ND'
            OH= 'OH'
            OK= 'OK'
            OR= 'OR'
            MD= 'MD'
            MA= 'MA'
            MI= 'MI'
            MN= 'MN'
            MS= 'MS'
            MO= 'MO'
            PA= 'PA'
            RI= 'RI'
            SC= 'SC'
            SD= 'SD'
            TN= 'TN'
            TX= 'TX'
            UT= 'UT'
            VT= 'VT'
            VA= 'VA'
            WA= 'WA'
            WV= 'WV'
            WI= 'WI'
            WY= 'WY'
        
 #----------------------------------------------------------------------------#
# Forms.
#----------------------------------------------------------------------------#
           
class ShowForm(Form):
    artist_id = StringField(
        'artist_id',validators=[DataRequired(),Regexp('^[0-9]*$',message='Only numbers are allowed')]
    )
    venue_id = StringField(
        'venue_id',validators=[DataRequired(),Regexp('^[0-9]*$',message='Only numbers are allowed')]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )
class VenueForm(Form):
  
    name = StringField(
        'name', validators=[DataRequired(),Length(min=5,max=300,message='leangth must be more than 5 and less than 300')]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],choices= [(choice.name, choice.value) for choice in State]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )  
    phone = StringField(
        'phone', validators=[DataRequired(),Regexp('^[0-9]*$',message='Only numbers are allowed')]
    )
    image_link = StringField(
        'image_link',validators=[DataRequired(),URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],choices= [(choice.name, choice.value) for choice in genres]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
       'website', validators= [URL(),DataRequired(message='Mandatory Field')]
    )
    seeking_talent = RadioField(
        'seeking_talent', choices=[('True','Yes'), ('False','No')]
    )
    seeking_description = TextAreaField(
        'seeking_description', validators=[] 
    )
class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],choices= [(choice.name, choice.value) for choice in State]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone',validators=[DataRequired(),Regexp('^[0-9-]*$',message='Only numbers are allowed Format '' xxx-xxx-xxxx ''' )]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],choices= [(choice.name, choice.value) for choice in genres]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    website = StringField(
       'website', validators= []
    )
    seeking_venue = RadioField(
        'seeking_talent', choices=[('True','Yes'), ('False','No')]
    )
    seeking_description = TextAreaField(
        'seeking_description', validators=[] 
    )
# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
