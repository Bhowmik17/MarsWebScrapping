#import dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from selenium import webdriver
import os
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)
    
def scrape():
    browser = init_browser()
    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)
    time.sleep(2)

    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # #### Find the latest Mars News Title and Paragraph Text(1)
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

    # Add the news date, title and summary to the dictionary
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

    # #### JPL Mars Space Images(2)
    # While chromedriver is open go to JPL's Featured Space Image page. 
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `featured_image_url`
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    
    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url

    # #### Mars Weather(3)
    # get mars weather's latest tweet from the website
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    # Scrape the browser into soup and use soup to find the weather tweet
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    # Add the weather tweet to the dictionary
    mars_data["mars_weather"] = mars_weather

    # #### Mars Facts(4)

    url4 = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url4)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    
    # Add the Mars facts table to the dictionary
    mars_data["mars_facts_table"] = mars_html_table     

    # #### Mars Hemisperes(5)

    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemis=[]

# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = mars_hemis
    # Return the dictionary
    return mars_data

