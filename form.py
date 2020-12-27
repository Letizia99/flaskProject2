from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, SelectField, FileField, TextAreaField, BooleanField
from wtforms.validators import DataRequired,Email,Length,ValidationError, EqualTo
from wtforms.fields.html5 import DateField

import email_validator
from model import User



class formRegistration(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=3,max=25)])
    surname=StringField('Surname', validators=[DataRequired(), Length(min=3, max=25)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    nationality=StringField('Nationality',validators=[DataRequired(),Length(min=3,max=25)])
    password=PasswordField('New Password',validators=[DataRequired()])
    password_con = PasswordField('Confirm your password',validators=[EqualTo('password')])
    submit=SubmitField('Register')

    def validate_email(self,email):
        user_check=User.query.filter_by(username=self.email.data).first()
        if user_check is not None:
            raise ValidationError('This email address is not valid or has been already registered')

class formLogin(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

'''class CreateEvent(FlaskForm):
    name = StringField('Event name:', validators=[DataRequired(), Length(min=2, max=20)])
    surename = StringField('Surename:', validators=[DataRequired(), Length(min=2, max=20)])
    location = StringField('Place:', validators=[DataRequired(), Length(min=2, max=30)])
    participants = StringField('Number of participants:', validators=[DataRequired(), Length(min=2, max=20)])
    date = DateField('Date', format='%d/%m/%Y' )
    hour = SelectField('Hour', coerce=int,choices=timechoices, default=29)
    description = StringField('Event description:', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Create')'''


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
    message = TextAreaField('Message',validators=[Length(min=6, max=500)])
    submit = SubmitField('Send message')


