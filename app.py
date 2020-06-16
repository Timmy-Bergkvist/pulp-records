import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from email_validator import validate_email, EmailNotValidError
from forms import LoginForm, RegistrationForm
from flask_toastr import Toastr
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'pulpRecordsDB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mongo = PyMongo(app)
toastr = Toastr(app)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Document):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/get_genra')
@login_required
def get_genra():
    return render_template('records.html', 
                           reviews=mongo.db.reviews.find())


@app.route('/add_records')
@login_required
def add_records():
    return render_template('addrecords.html', 
                           genra=mongo.db.genra.find())


@app.route('/insert_reviews', methods=['POST'])
@login_required
def insert_reviews():
    reviews =  mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    return redirect(url_for('get_genra'))



@app.route('/show_records')
@login_required
def show_records():
    total = mongo.db.reviews.count_documents({})
    return render_template('records.html')


@app.route('/records')
@login_required
def records():
    return render_template("records.html")


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.username)
    

#Delete user

@app.route('/delete_profile/<user_id>')
@login_required
def delete_user(user_id):
    #username = current_user.username
    #mongo.db.users.remove({'_id': ObjectId(user_id)})
    #session.clear()
    return render_template(url_for('index'))


#Registration

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are currently logged in!', 'info')
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one(
            {"username": form.username.data.lower() })
        existing_email = mongo.db.users.find_one(
            {"email": form.email.data})

        if existing_user is None and existing_email is None:
            password = generate_password_hash(request.form['password'], method='sha256')
            mongo.db.users.insert_one({
                                'username': request.form['username'].lower(),
                                'email': request.form['email'],
                                'password': password
            })

            flash(f'{form.username.data.lower()}, you are now a registered!', 'success')
            return redirect(url_for('login'))

        elif existing_user is not None:
            flash('Username is already in use.', 'warning') 
        else:
            flash('Email is already in use.', 'warning')
            
    return render_template('register.html', form=form)



#Callback used to reload the user object from the username 

@login_manager.user_loader
def load_user(username):
    u = mongo.db.users.find_one({"username": username})
    if not u:
        return None
        
    return User(u['username'])



#Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are logged in!', 'info')
        return redirect(url_for('profile'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = mongo.db.users.find_one({"username": form.username.data.lower()})
        if user and User.check_password(user['password'], form.password.data):
            user_obj = User(user['username'])
            login_user(user_obj)

            flash("You logged in", 'success')
            return redirect(url_for('profile'))

        elif user is None:
            flash("Username does not exist.", 'warning')
        else:
            flash("Wrong password.", 'error')

    return render_template('login.html', form=form)


#Logout

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/view_record')
@login_required
def view_record():
    return render_template('viewrecords.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
