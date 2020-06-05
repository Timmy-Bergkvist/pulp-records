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

@app.route('/records')
def records():
    return render_template("records.html")


@app.route('/add_records')
def add_records():
    return render_template("addrecords.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/log_out')
def log_out():
    return render_template("logout.html")



@app.route('/get_reviews')
def get_reviews():
    return render_template('records.html', 
                           reviews=mongo.db.reviews.find())



@app.route('/insert_genra', methods=['POST'])
def insert_genra():
    tasks =  mongo.db.genra
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_reviews'))




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
