from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser
    mars_data = {}
    

    # insert scraping code

    # mars_data['news_title'] = news_title
    # mars_data['news_p'] = news_p
    # mars_data['featured_image_url'] = featured_image_url
    # mars_data['mars_weather'] = mars_weather
    # mars_data['mars_facts'] = mars_facts
    # mars_data['img_title'] = img_title
    # mars_data['img_url'] = img_url

    return mars_data


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars_mongo = mongo.db.collection.find_one()
    render render_template("index.html", mars=mars_mongo)

@app.route("/scrape")
def scrape():
    mars_data = scrape.scrape_info()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

