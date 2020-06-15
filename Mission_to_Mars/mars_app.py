from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# from flask_pymongo import PyMongo

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# import pymongo
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# mars_db = client.mars
# mars_db.mars.insert_many(mars_data)

@app.route("/")
def home():
    mars_mongo = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_mongo)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

