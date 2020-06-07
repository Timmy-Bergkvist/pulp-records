import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'pulpRecordsDB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/get_genra')
def get_genra():
    return render_template('records.html', 
                           reviews=mongo.db.reviews.find())


@app.route('/add_records')
def add_records():
    return render_template('addrecords.html', 
                           genra=mongo.db.genra.find())


@app.route('/insert_reviews', methods=['POST'])
def insert_reviews():
    reviews =  mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    return redirect(url_for('get_genra'))



@app.route('/records')
def records():
    return render_template("records.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/log_out')
def log_out():
    return render_template("logout.html")






if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
