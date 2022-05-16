"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from __future__ import division
from http.client import UNAUTHORIZED

import flask_login
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, PredictForm, ReportForm, CreateForm, VerifyForm
from app.models import UserProfile, Reports, Admin
from werkzeug.security import check_password_hash
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from app import mail
from flask_mail import Message
import random
###
# Routing for your application.
###

#Global
data=[]

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


def getReports():
    reports = Reports.query.filter_by(userid=current_user.get_id()).all()
    records=[{"id":r.reportid,
        "division":r.division,
        "city":r.city,
        "crime":r.crime,
        "date":r.date,
        "time":r.time,
        "details":r.details} for r in reports]
    return records

@app.route('/notification')
@login_required
def notify():
    
    """Render a secure page on our website that only logged in users can access."""
    user_reports=getReports()


    return render_template('notification.html', report=user_reports)

@app.route('/show_reports')
@login_required
def showReports():
    if 'user' in session:
        u = session['user']
        session.pop('user',None)
        if u == 'admin':
            reports = Reports.query.all()
            records=[{"id":r.reportid,
            "division":r.division,
            "city":r.city,
            "crime":r.crime,
            "date":r.date,
            "time":r.time,
            "details":r.details} for r in reports]
            session['user']='admin'
        if u=='reg':
            session['user']='reg'
            return ('UNAUTHORIZED', 'danger')
    return render_template('show_reports.html', report=records)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if user is already logged in, just redirect them to our secure page
        # or some other page like a dashboard
        return redirect(url_for('dashboard'))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    # Login and validate the user.
    if form.validate_on_submit():
        # Query our database to see if the username and password entered
        # match a user that is in the database.
        email = form.email.data
        password = form.password.data

        

        user = UserProfile.query.filter_by(email=email).first()
        
        


        if user is not None and check_password_hash(user.password, password):
            session['user']='reg'
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True

        

            # If the user is not blank, meaning if a user was actually found,
            # then login the user and create the user session.
            # user should be an instance of your `User` class
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        
        if user is None:
            user = Admin.query.filter_by(email=email).first()
            
            session['user']='admin'
            remember_me=False
            if user is not None and check_password_hash(user.password, password):
                print('admin pswd: ',user.email)
                remember_me = False
                login_user(user)
                flash('Logged in successfully.', 'success')

                next_page = request.args.get('next')
                return redirect(next_page or url_for('showReports'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)
    
def generateCode():
    code= random.randrange(100000,999999)
    return code

@app.route('/create-account', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email=form.email.data
            password=form.password.data
            password2=form.password2.data
            code = generateCode()
            session['response']=str(code)
            data.append(email) 
            data.append(password)
            subject= "Email Verification Code"
            name = "Crime Predictors"
            msg = Message(subject, sender =(name,'noreply@demo.com'), recipients=[email])
            msg.body = 'Your verification code is ' + str(code)
            print("hello3")
            mail.send(msg)
            return redirect(url_for('verify'))
        flash_errors(form)
    return render_template('create_account.html', form=form)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form=VerifyForm()
    if request.method == "POST":
        if form.validate_on_submit():
            number= request.form['code']
            print(number)

            if 'response' in session:
            
                email=data[0]
                password=data[1]
                s = session['response']
                session.pop('response',None)
                if s == str(number):
                
                    form_data=UserProfile(email, password)
                    #form_data.email=email
                    #form_data.password=password
                    #form_data=Admin(email, password)
                    

                    db.session.add(form_data)
                    db.session.commit()
                    flash('Account successfully created!')
                    return redirect(url_for('login'))

    return render_template('verify.html', form=form)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    div_arr= ['Allman Town', 'Barbican', 'Belfield', 'Black River' , 'Braeton', 'Bridgeport', 'Browns Town', 'Buff Bay', 'Cassia Park', 'Cedar Valley', 'Chancery Hill', 'Chester Castle', 'Christiana', 'De La Vega City', 'Denham Town', 'Duhaney Park', 'Edgewater', 'Ensom City', 'Falmouth', 'Frome', 'Gordon Town', 'Greater Portmore North', 'Green Island', 'Greenwich Town', 'Gregory Park', 'Hagley Park', 'Harbour View', 'Havendale', 'Hayes', 'Hellshire', 'Highgate', 'Hopewell', 'Independent City', 'Junction', 'Kintyre', 'Lacovia', 'Lauriston', 'Lawrence Tavern', 'Lluidas Vale', 'Lorrimers', 'Lucea', 'Mandeville', 'Martha Brae', 'Mavis Bank', 'Maxfield Park', 'May Pen East', 'May Pen North', 'Mile Gully', 'Mocho', 'Molynes Gardens', 'Mona', 'Moneague', 'Montego Bay Central', 'Montego Bay North', 'Montego Bay North East', 'Montego Bay South East', 'Montego Bay West', 'Morant Bay', 'Negril', 'Norbrook', 'Ocho Ríos', 'Old Harbour Central', 'Old Harbour North', 'Olympic Gardens', 'Oracabessa','Papine', 'Payne Lands', 'Petersfield', 'Point Hill', 'Port Antonio', 'Port Maria', 'Portmore Pines', 'Porus', 'Race Course', 'Rae Town', 'Red Hills', 'Richmond', 'Richmond', 'Rocky Point', 'Saint Anns Bay', 'Sandy Bay', 'Santa Cruz', 'Savanna-La-Mar', 'Savanna-La-Mar North', 'Seaforth', 'Seaview Gardens', 'Sherwood Content', 'Spanish Town', 'Springfield', 'Spur Tree', 'Stony Hill', 'Tivali Gardens', 'Trafalgar', 'Trench Town', 'Twickenham Park', 'Vineyard Town', 'Waterford', 'Waterhouse', 'Waterloo', 'Whitehall', 'Yallahs']
    model = pickle.load(open('model.pkl', 'rb'))
    form = PredictForm()
    # Login and validate the user.
    if request.method == "POST":
        if form.validate_on_submit():
            division= form.division.data
            month = form.month.data
            crime = form.crime.data
            
            index = div_arr.index(division)
            new_arr= [0]*100
            new_arr[index] = 1
            new_arr.insert(0, month)
            new_arr.insert(1, crime)

            prediction = model.predict([new_arr])
            output = round(prediction[0], 5) 
            output = output*100
            key1 = 'rate ≥ 25% ----> [HOTSPOT ZONE]'
            key2 = '24.99% ≥ rate ≥ 18% ----> [MODERATE ZONE]'
            key3 = '17.99% ≥ rate ≥ 10% ----> [NEUTRAL ZONE]'
            key4 = 'rate < 10% ----> [SAFE ZONE]'
            flash('Crime rate prediction is: {}%'.format(output))
            flash(key1)
            flash(key2)
            flash(key3)
            flash(key4)
            flash('Division selected: {}'.format(division))
            flash('Month selected: Month {}'.format(month))
            flash('Type of crime selected: Crime number {}'.format(crime))
            return redirect(url_for("predict"))
            
        flash_errors(form)
    return render_template('predict_form.html', form=form)


    flash_errors(form)
    return render_template('predict_form.html', form=form)

@app.route("/news")
def news():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.jamaicaobserver.com/section/latest-news/')

    results = []

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    driver.quit()

    for element in soup.findAll(attrs='col-12 col-md-6 article-wrapper'):
        image=element.find('img').get('src') 
        #if image not in results:
        #    results.append(image)
        title=element.find(attrs='headline').find('a')

        #if title not in results:
        #    results.append(title.text)
    
        pub=element.find(attrs='pubdate')

        #if pub not in results:
         #   results.append(pub.text)
        
        lynk=element.find(attrs='headline').find('a').get('href')
        record={'image':image, 'title':title.text, 'pub':pub.text, 'link':lynk}
        results.append(record)
    print(results)
    return render_template('news.html', lst=results)

@app.route('/report',methods=['GET','POST'])
@login_required
def report():
    """Initialization of report form."""
    form = ReportForm()
    
    if form.validate_on_submit():
        
        division=form.division.data
        city=form.city.data
        date=form.date.data
        time=form.time.data
        details=form.details.data
        crime=form.crime.data

        if current_user.is_authenticated():
            uid = current_user.get_id()
            userid=uid

        form_data=Reports(division, city, crime, date, time, details, userid)   

        db.session.add(form_data)
        db.session.commit()
        flash('Report successfully logged!')
        return redirect(url_for('notify'))
        

    return render_template('report.html', form=form)

@app.route('/dashboard')
def dashboard():
    """Initialization of dashboard form"""
    return render_template('dashboard.html')
    
@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))


# This callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


# Flash errors from the form if validation fails with Flask-WTF
# http://flask.pocoo.org/snippets/12/
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
