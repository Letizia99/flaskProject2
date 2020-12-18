from flask import Flask,render_template,redirect,url_for,session, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY']='sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

from model import User
from form import formRegistration,loginForm



@app.route('/', methods=['POST', 'GET'])
def login():
    login_form = loginForm()
    if login_form.validate_on_submit():
        user_info = User.query.filter_by(username=login_form.username.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, login_form.password.data):
            session['user_id'] = user_info.id
            session['name'] = user_info.name
            session['email'] = user_info.username
            return redirect('index')
    else:
        return render_template('login.html', login_form=login_form)


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



@app.route('/registerdb',methods=['POST','GET'])
def registerPagedb():
    name=None
    registerForm=formRegistration()
    if request.method=='POST':
        if registerForm.validate():
            name=registerForm.name.data
            session['name']=registerForm.name.data
            session['email']=registerForm.email.data
            password_2 = bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8')
            newuser = User(name=registerForm.name.data, username=registerForm.email.data, password=password_2, role_id=2)
            db.session.add(newuser)
            db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('register-db.html', registerForm=registerForm, name_website='CUKT-Feels like home', name=name)



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