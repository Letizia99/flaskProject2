from flask import Flask,render_template,redirect,url_for,session, request, flash, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required

from flask_bcrypt import Bcrypt
import os

basedir=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']='sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
auth = Blueprint('auth', __name__)

from model import User
from form import formRegistration, formLogin



@app.route('/', methods=['POST', 'GET'])
def login():
    login_form = formLogin()
    if login_form.validate_on_submit():
        user_info = User.query.filter_by(username=login_form.username.data).first()
        if user_info is not None and bcrypt.check_password_hash(user_info.password, login_form.password.data):
            login_user(User, login_form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('homepage')
            return redirect(next)
        flash('Invalid username or password.')
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
            newuser = User(username=registerForm.name.data, name=registerForm.name.data, surname=registerForm.surname.data, nationality=registerForm.nationality.data, password=bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8'))
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('homepage'))
        else:
            print "There is an error in your input data"
    else:
        return render_template('register-db.html', registerForm=registerForm, name_website='CUKT-Feels like home')


@app.route('/homepage')
def homepage():
    return render_template('index.html')

@app.route('/profile')
def profilepage():
    return render_template('profilepage.html')

@app.route('/cukt')
def cuktpage():
    return render_template('CUKT.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500



@app.route('/dashboard')
def dashboard():
    if session.get('email'):
        name=session.get('name')
        return render_template('dashboard.html',name=name)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('templatehtml')) # =>redirect(index)



if __name__ == '__main__':
    app.run()