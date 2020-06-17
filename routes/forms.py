import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter a valid username"), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password"), Length(min=8, max=80)])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Username required to complete registration process"), Length(min=4, max=15)])
    email = StringField('Email', validators=[DataRequired("Email address required to complete registration process"), Email("This is not a valid email address"), Length(min=8, max=30)])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password"), Length(min=8, max=80)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired("Repeat Password"), EqualTo('password')])
    submit = SubmitField('Sign Up')