import os
from flask import Flask, render_template, redirect, request, url_for
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from email_validator import validate_email, EmailNotValidError
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

db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Document):
    meta = {'collection': '<---YOUR_COLLECTION_NAME--->'}
    email = db.StringField(max_length=30)
    password = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])



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
def insert_reviews():
    reviews =  mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    return redirect(url_for('get_genra'))


@app.route('/records')
@login_required
def records():
    return render_template("records.html")


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.email)


#Registration

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.email.data,hashpass).save()
                login_user(hey)
                return redirect(url_for('profile'))
    return render_template('register.html', form=form)


#Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('profile'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('profile'))
    return render_template('login.html', form=form)



#Logout

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
