from flask import Flask,render_template,redirect,url_for,session, request, flash, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

basedir=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']='sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)


from model import User,SocialEatingEvent, SharedMeal
from form import formRegistration, formLogin, Contactus, formCreateEvent, JoinEvent, formShareMeal, formSearchMeal



@app.route('/', methods=['POST', 'GET'])
def login():
    login_form = formLogin()
    if login_form.validate_on_submit():
        user_info = User.query.filter_by(email=login_form.email.data).first()
        if user_info is not None:
            user_info.password == login_form.password.data
            login_user(user_info, remember=login_form.remember_me.data)
            return redirect('homepage')
        return flash('Invalid email or password.')
    return render_template('login.html', login_form=login_form)

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@app.route('/registerdb',methods=['POST','GET'])
def registerPagedb():
    registerForm=formRegistration()
    if request.method=='POST':
        if registerForm.validate():
            newuser = User(email=registerForm.email.data, name=registerForm.name.data, surname=registerForm.surname.data, nationality=registerForm.nationality.data, password=bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8'))
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('homepage'))
        flash("There is an error in your input data", category='danger')
    return render_template('register-db.html', registerForm=registerForm, name_website='CUKT-Feels like home')


@app.route('/homepage')
@login_required
def homepage():
    return render_template('index.html', name=current_user.email)


@app.route('/profilepage')
@login_required
def profilepage():
    return render_template('profilepage.html', name=current_user.email)

@app.route('/cukt')
def cuktpage():
    return render_template('index.html')


@app.route('/contactus', methods=['POST', 'GET'])
def contactus():
    name = None
    contactForm = Contactus()
    if contactForm.validate_on_submit():
        session['name'] = contactForm.name.data
        name = contactForm.name.data
        return redirect('dashboard')
    return render_template('contact.html', contactForm=contactForm, name=name)

@app.route('/dashboard')
def dashboard():
    if session.get('name'):
        return render_template('dashboardcontact.html')
    else:
        return redirect('contactus')

@app.route('/createevent', methods=['POST', 'GET'])
def createEvent():
    createForm = formCreateEvent()
    if request.method=='POST':
        if createForm.validate_on_submit():
            newevent = SocialEatingEvent(title=createForm.title.data, timetable=createForm.timetable.data, date=createForm.date.data, price=createForm.price.data,menu=createForm.menu.data, numpeople=createForm.partecipants.data, location=createForm.location.data, description=createForm.description.data)
            db.session.add(newevent)
            db.session.commit()
            return redirect(url_for('booking'))
        flash("There is an error in your input data", category='danger')
    return render_template('create.html', createForm=createForm)

@app.route('/bookevent', methods=['POST', 'GET'])
def booking():
    name = None
    bookingForm = JoinEvent()
    if bookingForm.validate_on_submit():
        session['name'] = bookingForm.name.data
        session['date'] = bookingForm.date.data
        name = bookingForm.name.data
        return redirect('dashboard')
    return render_template('booking.html', bookingForm=bookingForm, name=name)

@app.route('/share', methods=['POST', 'GET'])
def share():
    shareForm = formShareMeal()
    if request.method=='POST':
        if shareForm.validate_on_submit():
            newmeal = SharedMeal(meal=shareForm.mealname.data, date=shareForm.date.data, price=shareForm.price.data, menu=shareForm.menu.data, location=shareForm.location.data,address=shareForm.address.data, description=shareForm.description.data)
            db.session.add(newmeal)
            db.session.commit()
            return redirect(url_for('booking'))
        flash("There is an error in your input data", category='danger')
    return render_template('sharemeal.html', shareForm=shareForm)

@app.route('/searchmeal', methods=['POST', 'GET'])
def searchmeal():
    name = None
    smealForm = formSearchMeal()
    if smealForm.validate_on_submit():
        session['name'] = smealForm.name.data
        session['date'] = smealForm.date.data
        name = smealForm.name.data
        return redirect('dashboard')
    return render_template('SearchMeal.html', smealForm=smealForm, name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()