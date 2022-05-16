from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, InputRequired, ValidationError
from wtforms import validators
import phonenumbers
#from flask_bootstrap import Bootstrap

parishlst=["--Select a parish--", 'Westmoreland', 'Hanover', 'St.James', 'St.Elizabeth', 'Manchester', 'Clarendon', 'St.Ann', 'Trelawny', 'St.Catherine', 'St.Mary', 'Kingston', 'St.Andrew', 'St.Thomas', 'Portland']
divlst=["--Select a division--",'Allman Town', 'Barbican', 'Belfield', 'Black River' , 'Braeton', 'Bridgeport', 'Browns Town', 'Buff Bay', 'Cassia Park', 'Cedar Valley', 'Chancery Hill', 'Chester Castle', 'Christiana', 'De La Vega City', 'Denham Town', 'Duhaney Park', 'Edgewater', 'Ensom City', 'Falmouth', 'Frome', 'Gordon Town', 'Greater Portmore North', 'Green Island', 'Greenwich Town', 'Gregory Park', 'Hagley Park', 'Harbour View', 'Havendale', 'Hayes', 'Hellshire', 'Highgate', 'Hopewell', 'Independent City', 'Junction', 'Kintyre', 'Lacovia', 'Lauriston', 'Lawrence Tavern', 'Lluidas Vale', 'Lorrimers', 'Lucea', 'Mandeville', 'Martha Brae', 'Mavis Bank', 'Maxfield Park', 'May Pen East', 'May Pen North', 'Mile Gully', 'Mocho', 'Molynes Gardens', 'Mona', 'Moneague', 'Montego Bay Central', 'Montego Bay North', 'Montego Bay North East', 'Montego Bay South East', 'Montego Bay West', 'Morant Bay', 'Negril', 'Norbrook', 'Ocho Ríos', 'Old Harbour Central', 'Old Harbour North', 'Olympic Gardens', 'Oracabessa','Papine', 'Payne Lands', 'Petersfield', 'Point Hill', 'Port Antonio', 'Port Maria', 'Portmore Pines', 'Porus', 'Race Course', 'Rae Town', 'Red Hills', 'Richmond', 'Richmond', 'Rocky Point', 'Saint Anns Bay', 'Sandy Bay', 'Santa Cruz', 'Savanna-La-Mar', 'Savanna-La-Mar North', 'Seaforth', 'Seaview Gardens', 'Sherwood Content', 'Spanish Town', 'Springfield', 'Spur Tree', 'Stony Hill', 'Tivali Gardens', 'Trafalgar', 'Trench Town', 'Twickenham Park', 'Vineyard Town', 'Waterford', 'Waterhouse', 'Waterloo', 'Whitehall', 'Yallahs']
monthlst=[(0,"--Select a month--"),(1,"January"),(2,"February"),(3,"March"),(4,"April"), (5,"May"),(6,"June"),(7,"July"),(8,"August"),(9,"September"),(10,"October"),(11,"November"),(12,"December")]
crimelst=[(0, "--Select a crime type--"),(1,"Aggravated Assault"),(2,'Larceny/Theft'),(3,'Murder'),(4,'Rape'),(5,'Robbery')]


class LoginForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')

class CreateForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    password2= PasswordField('Re-enter Password', [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match!')])

class PredictForm(FlaskForm):
    division= SelectField('Division', validators=[DataRequired()], choices=divlst)
    month= SelectField('Month', validators=[DataRequired()], choices=monthlst, coerce=int)
    crime= SelectField('Type of Crime', validators=[DataRequired()], choices=crimelst, coerce=int)


class ReportForm(FlaskForm):
    division = SelectField('Division', validators=[DataRequired()], choices=parishlst)
    city = TextAreaField('City/Town', validators=[DataRequired()])
    crime = SelectField('Type of Crime', validators=[DataRequired()], choices=crimelst)
    date = DateField('Date of Crime', validators=[DataRequired()])
    time = TimeField('Estimated Time of Crime', validators=[DataRequired()])
    details = TextAreaField('Details of Crime', validators=[DataRequired()])

class VerifyForm(FlaskForm):
    code = StringField('Enter 6-digit Code', validators=[DataRequired()])