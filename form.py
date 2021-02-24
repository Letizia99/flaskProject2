from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, SelectField, FileField, TextAreaField, BooleanField
from wtforms.validators import DataRequired,Email,Length,ValidationError, EqualTo
from wtforms.fields.html5 import DateField
import email_validator

from model import User



class formRegistration(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=3,max=25)])
    surname=StringField('Surname', validators=[DataRequired(), Length(min=3, max=25)])
    email=StringField('Email',validators=[DataRequired(),Email(),Length(min=4, max=50)])
    nationality=StringField('Nationality',validators=[DataRequired(),Length(min=3,max=15)])
    password=PasswordField('New Password',validators=[DataRequired(), Length(min=4, max=20)])
    password_con = PasswordField('Confirm your password',validators=[EqualTo('password')])
    submit=SubmitField('Register')

    def validate_email(self,email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('This email address is not valid or has been already registered')


class formLogin(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class formCreateEvent(FlaskForm):
    title = StringField('Event name:', validators=[DataRequired(), Length(min=2, max=20)])
    timetable = SelectField('Time of your event', validators=[DataRequired(), Length(min=2, max=20)], choices=[(''),('Lunch'),('Dinner')])
    price = StringField('Price:', validators=[DataRequired()])
    menu = SelectField('Menu:', validators=[DataRequired()], choices=[(''),('Vegan'),('Vegeterian'),('Neither')])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    partecipants = SelectField('Number of participants:', validators=[DataRequired()], choices=[(p, str(p)) for p in range(0,11)])
    description = StringField('Event description:', validators=[DataRequired(), Length(min=0, max=200)])
    location = SelectField('Location:', validators=[DataRequired()], choices=[(''),('Milano'),('Torino'),('Firenze'),('Napoli'),('Genova'),('Roma'),('Venezia')])
    submit = SubmitField('Create')

class JoinEvent(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=2, max=20)])
    time = StringField('Time:', validators=[DataRequired()])
    price = StringField('Price:', validators=[DataRequired()])
    location = StringField('Location:', validators=[DataRequired()])
    menu = StringField('Menu:', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    participants = StringField('Number of participants:', validators=[DataRequired()])
    submit = SubmitField('Search')

class formShareMeal(FlaskForm):
    mealname = StringField('Meal name:', validators=[DataRequired(), Length(min=2, max=20)])
    price = StringField('Price:', validators=[DataRequired()])
    description = StringField('Dish description:', validators=[DataRequired(), Length(min=2, max=200)])
    menu = SelectField('Menu:', validators=[DataRequired()],choices=[(''),('Vegan'),('Vegeterian'),('Neither')])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    location = SelectField('City:', validators=[DataRequired()], choices=[(''),('Milano'),('Torino'),('Firenze'),('Napoli'),('Genova'),('Roma'),('Venezia')])
    address = StringField('Address/District:', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Share')

class formSearchMeal(FlaskForm):
    location = StringField('Location:', validators=[DataRequired()])
    menu = SelectField('Menu:', validators=[DataRequired()], choices=[(''),('Vegan'),('Vegeterian'),('Neither')])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit=SubmitField('Search')


class Chatform(FlaskForm):
    description = StringField('Enter your message:', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Send message')

class Review(FlaskForm):
    description = StringField('Your description', validators=[DataRequired(), Length(min=2, max=200)])
    NumberofStars = SubmitField('Submit')
    image = FileField('file', validators=[DataRequired()])
    uploadImage = SubmitField('upload')
    submit = SubmitField('Submit')

class Remove(FlaskForm):
    submit = SubmitField('Remove')

class Contactus(FlaskForm):
    name = StringField('Name',validators=[Length(min=2, max=25)])
    email = StringField('Email Address',validators=[Length(min=6,max=35),Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=50)])
    message = TextAreaField('Message',validators=[Length(min=6, max=500)])
    submit = SubmitField('Send message')


