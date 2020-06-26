import os
import re
"""
Cloudinary API imports
"""
import cloudinary as Cloud
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload
import cloudinary.api
from cloudinary.utils import cloudinary_url

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from utility.forms import LoginForm, RegistrationForm
from utility.user import User
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from email_validator import validate_email, EmailNotValidError
from flask_paginate import Pagination, get_page_args, get_page_parameter
from utility.flask_toastr import Toastr
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'pulpRecordsDB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

Cloud.config.update = ({
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})

mongo = PyMongo(app)
toastr = Toastr(app)
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# INDEX
'''
Function with a route that will
direct you to home page.
'''


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Displays the fourth latest added records.
    records = mongo.db.recordCollection.find().sort([('timestamp', -1)]).limit(4)
    return render_template("index.html", records=records)


# REGISTER
"""
Registration function that enables user to
register and create an user account.
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are currently logged in!', 'info')
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Register a unique username and email.
        # Checks if the username and email already exist.
        existing_user = mongo.db.users.find_one({"username": form.username.data})
        existing_email = mongo.db.users.find_one({"email": form.email.data})
        # If the username and email dont exist create a username, email and password.
        if existing_user is None and existing_email is None:
            password = generate_password_hash(request.form['password'], method='sha256')
            mongo.db.users.insert_one({
                                'username': request.form['username'],
                                'email': request.form['email'],
                                'password': password
            })

            flash(f'{form.username.data}, you are now a registered!', 'success')
            return redirect(url_for('login'))

        elif existing_user is not None:
            flash('Username is already in use.', 'warning')
        else:
            flash('Email is already in use.', 'warning')
    return render_template('register.html', form=form)


# LOGIN
"""
Function that logs in the user
and Checks the password is correct.
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are logged in!', 'info')
        return redirect(url_for('profile'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = mongo.db.users.find_one({"username": form.username.data})
        # Checks if the password is correct.
        if user and User.check_password(user['password'], form.password.data):
            user_obj = User(user['username'])
            login_user(user_obj)

            flash("You logged in", 'success')
            return redirect(url_for('index'))

        elif user is None:
            flash("Username does not exist.", 'warning')
        else:
            flash("Wrong password.", 'error')

    return render_template('login.html', form=form)


# USER LOADER
"""
Callback used to reload the user
object from the username.
"""


@login_manager.user_loader
def load_user(username):
    u = mongo.db.users.find_one({"username": username})
    if not u:
        return None
    return User(u['username'])


# LOGOUT
"""
Function that logs out user.
"""


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# PROFILE
"""
Function that displays username, email
and displays all added records.
"""


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = mongo.db.users.find_one({'username': username})

    users_records = mongo.db.recordCollection.find({'added_by': username}).sort([("_id", -1)])
    return render_template("profile.html", user=user, recordCollection=users_records)


# DELETE PROFILE
"""
Function that delete the profile and
all records added by the current user.
"""


@app.route('/delete_profile/<user_id>')
@login_required
def delete_profile(user_id):
    username = current_user.username
    # All records will be deleted by the current user who inserted the records
    mongo.db.recordCollection.remove({'added_by': username})
    # Remove user
    mongo.db.users.remove({'_id': ObjectId(user_id)})
    session.clear()

    flash('Your account has been successfully deleted.', 'success')
    return redirect(url_for('index'))


# EDIT RECORDS
"""
Function that allows the
current user to edit a record.
"""


@app.route('/edit_record/<record_id>')
@login_required
def edit_record(record_id):
    the_record = mongo.db.recordCollection.find_one({"_id": ObjectId(record_id)})
    the_genre = mongo.db.genre.find()
    return render_template('editrecord.html', record_id=record_id, record=the_record, genre=the_genre)


# UPDATE RECORDS
"""
Function that updates all
the information in the form.
"""


@app.route('/update_record/<record_id>', methods=['GET', 'POST'])
@login_required
def update_record(record_id):
    recordCollection = mongo.db.recordCollection
    username = current_user.username
    # Update record title and genre
    record_title = request.form['record_title'].title()
    genre_name = request.form['genre_name'].title()
    # Updade image
    image_id = generate_image(request.form.get('image_id'))
    # Update record information
    recordCollection.update({'_id': ObjectId(record_id)}, {
        'genre_name': request.form.get('genre_name').title(),
        'artist_name': request.form.get('artist_name'),
        'record_title': request.form.get('record_title').title(),
        'image_id': request.form.get('image_id'),
        'tracklist': request.form.get('tracklist'),
        'added_by': request.form.get('added_by'),
        'record_description': request.form.get('record_description')
        })
    flash('Records have been updated!', 'success')
    return redirect(url_for('records', record_id=record_id,))


# DELETE RECORD
"""
Function that allows the
current user to delete a record.
"""


@app.route('/delete_record/<record_id>')
def delete_record(record_id):
    mongo.db.recordCollection.remove({'_id': ObjectId(record_id)})
    flash('Record have been deleted!', 'success')
    return redirect(url_for('records'))


# INSERT RECORD
"""
Function that inserts the record
information to records template page.
"""


@app.route('/insert_records', methods=['POST'])
@login_required
def insert_records():
    recordCollection = mongo.db.recordCollection
    username = current_user.username

    record_title = request.form['record_title'].title()
    genre_name = request.form['genre_name'].title()

    # Check if record with a given author and title already exists
    existing_record = mongo.db.recordCollection.count_documents({'$and': [{'record_title': record_title}, {'genre_name': genre_name}]})
    # Generate cover image link
    image_id = generate_image(request.form.get('image_id'))
    # If record does not exist in the collection insert it
    if existing_record == 0:
        recordCollection.insert_one({
            'genre_name': request.form['genre_name'].title(),
            'artist_name': request.form['artist_name'],
            'record_title': request.form['record_title'].title(),
            'image_id': image_id,
            'added_by': username,
            'tracklist': request.form['tracklist'],
            'record_description': request.form['record_description']
        })
        flash('Your record has now been successfully added.', 'success')
    else:
        flash('Record already exists!', 'error')
    return redirect(url_for('records'))


# ADD RECORD TEMPLATE
"""
Function that renders add records template.
From her the genre database is connected.
"""


@app.route('/add_records/<username>', methods=['GET', 'POST'])
@login_required
def add_records(username):
    user = mongo.db.users.find_one({'username': username})
    return render_template('addrecords.html', user=user, genre=mongo.db.genre.find())


# RECORD IMAGE
"""
Record image Generate image placeholder
in cases when use does not provide a link.
If no image is provided a link from
cloudinary will display no image record img.
"""


def generate_image(image_input):
    # if no image is provided
    image_id = "https://res.cloudinary.com/dpctylyfk/image/upload/v1592383030/music%20images/no-image_bwbufa.jpg"
    if image_input == '':
        image_id = image_id
    if any(re.findall(r'jpeg|jpg|png', image_input, re.IGNORECASE)):
        image_id = image_input
    else:
        image_id
    return image_id


# RECORDS
"""
Function that displays all records.
"""


@app.route('/records')
def records():
    return render_template('records.html', recordCollection=mongo.db.recordCollection.find())


# VIEW RECORD
"""
Function that displays a record when a
user click on a record in the records template.
"""


@app.route('/view_record/<record_id>')
def view_record(record_id):
    the_record = mongo.db.recordCollection.find_one({'_id': ObjectId(record_id)})

    return render_template('viewrecord.html', record=the_record)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=False)
