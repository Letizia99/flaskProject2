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


class CreateEvent(FlaskForm):
    title = StringField('Event name:', validators=[DataRequired(), Length(min=2, max=20)])
    time = StringField('Time:', validators=[DataRequired(), Length(min=2, max=20)])
    price = StringField('Price:', validators=[DataRequired(), Length(min=2, max=5)])
    menu = StringField('Menu:', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    participants = StringField('Number of participants:', validators=[DataRequired()])
    description = StringField('Event description:', validators=[DataRequired(), Length(min=0, max=200)])
    location = StringField('Location:', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Create')


class ShareMeal(FlaskForm):
    mealName = StringField('Meal name:', validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Event description:', validators=[DataRequired(), Length(min=2, max=200)])
    recipe = StringField('Recipe:', validators=[DataRequired(), Length(min=2, max=500)])
    date = StringField('Date:', validators=[DataRequired(), Length(min=2, max=20)])
    image= FileField('file',validators=[DataRequired()])
    uploadImage= SubmitField('upload')
    submit = SubmitField('Create')

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


