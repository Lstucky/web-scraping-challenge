from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    mars_data = {}

    # news  title and paragraph
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    news_html = bs(browser.html, 'html.parser')
    results1 = news_html.find('ul', class_="item_list")
    news_title = results1.find('div', class_='content_title').text
    news_p = results1.find('div', class_='article_teaser_body').text

    # full image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    full_image = browser.find_by_id("full_image")
    full_image.click()
    next_image = browser.find_link_by_partial_text('more info')
    next_image.click()
    featured_html = bs(browser.html, 'html.parser')
    featured_image_url = featured_html.select_one('figure.lede a img').get('src')
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    # twitter weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(4)
    twitter_html = bs(browser.html, 'html.parser')
    tweets = twitter_html.find('section', attrs={"aria-labelledby": 'accessible-list-0'})
    tweet = tweets.find_all('span')
    all_tweets = []
    for x in tweet:
        twt = x.text
        if len(twt)>100:
            all_tweets.append(twt)
    mars_weather = all_tweets[1]

    # table data
    table_url = 'https://space-facts.com/mars/'
    table = pd.read_html(table_url)
    table1_df = table[0]
    table1_df = table[0]
    table1_df.columns = ['Description', 'Value']
    table1_df.set_index('Description', inplace=True)
    html_table1 = table1_df.to_html()
    mars_facts = html_table1.replace('\n', '')

    # start mars data dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_facts,
        'img_title': [],
        'img_url': []
    }

    # hemisphere images and titles, append mars_data dictionary
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    hemi_html = bs(browser.html, 'html.parser')
    links = []
    title = []
    for l in hemi_html.find_all('a', class_='itemLink'):
        if l['href'] not in links:
            links = 'https://astrogeology.usgs.gov/' + l['href'] + '.tif/full.jpg'
            print(links)
            mars_data['img_url'].append(links)
    for t in hemi_html.select('a.itemLink h3'):
        if t.text not in title:
            title = t.text
            print(title)
            mars_data['img_title'].append(title)

    browser.quit()

    return mars_data


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():
    mars_mongo = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_mongo)

@app.route("/scrape")
def scrape_something():
    mars_data = scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

