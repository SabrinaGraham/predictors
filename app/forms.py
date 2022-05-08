from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, InputRequired, ValidationError
import phonenumbers
from flask_bootstrap import Bootstrap

parishlst=["--Select a parish--","Kingston","St.Andrew","Portland", "St.Thomas","St.Catherine", "St.Mary", "St.Ann", "Manchester", "Clarendon", "Hanover", "Westmoreland", "St.James", "Trelawny", "St.Elizabeth"]
monthlst=["--Select a month--","January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
crimelst=["--Select a crime type--","Homocide","Assault and Battery", "Kidnaping", "Sex Crimes", "Traffic Offenses", "Theft Crimes", "Drug Crimes", "Fraud"]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')

class PredictForm(FlaskForm):
    division= SelectField('Parish', validators=[DataRequired()], choices=parishlst)
    month= SelectField('Month', validators=[DataRequired()], choices=monthlst)
    crime= SelectField('Type of Crime', validators=[DataRequired()], choices=crimelst)

class PhoneForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
class ReportForm(FlaskForm):
    division = SelectField('Parish', validators=[DataRequired()], choices=parishlst)
    city = TextAreaField('City/Town', validators=[DataRequired()])
    crime = SelectField('Type of Crime', validators=[DataRequired()], choices=crimelst)
    date = DateField('Date of Crime', validators=[DataRequired()])
    time = TimeField('Estimated Time of Crime', validators=[DataRequired()])
    details = TextAreaField('Details of Crime', validators=[DataRequired()])