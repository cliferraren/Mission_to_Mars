#Import Dependencies needed to scrape HTML
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs


#Function to init browser to Chrome
def init_browser():
    executable_path = {"executable_path": "/Users/rck/chrome_driver/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#Function to scrape the Latest News Article from NASA
#get only the first(latest) article
#1st scrape method declared   
def get_news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    #try catch block to catch if error is encountered, pass will return the title and paragraph element of the article
    try:
        browser.visit(url)
        html_string = browser.html

        #The 'html.parser' argument indicates that we want to do the parsing using Python’s built-in HTML parser.
        soup = bs(html_string, 'html.parser')

        div = soup.find('div', attrs={'class': 'list_text'})
        title=div.findNext('div', {'class': 'content_title'}).text            
        description=div.findNext('div', {'class': 'article_teaser_body'}).text
    except:
        pass
    return {"news_title":title,"news_p":description}

#Function to scrape the image URL from JPL page
#2nd scrape method declared 
def get_featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #try catch block to catch if error is encountered, pass will return image URL
    try:
        browser.visit(url)
        button = browser.find_by_id("full_image")
        button.click()
        time.sleep(2) # will pause the execution of the loop for a specified amount of seconds

        html_string = browser.html
        soup = bs(html_string, 'html.parser')
        anchor = soup.find('a','ready')
        if anchor.img:
            image_url = anchor.img['src']
        featured_image_url = "https://www.jpl.nasa.gov" + image_url      
    except:
        pass
    return featured_image_url

#Function to get latest weather update from Twitter
#3rd scrape method declared 
def get_latest_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'

    #try catch block to catch if error is encountered, pass will return latest weather update
    try:
        browser.visit(url)
        html_string = browser.html
        soup = bs(html_string, 'lxml')
        
        latest_weather = soup.find('div','js-tweet-text-container').text.strip()
    except:
        pass
    return latest_weather 

#Function to get Mars Facts information from Mars Facts webpage
#4th scrape method declared 
def get_facts(browser):
    url = 'https://space-facts.com/mars/'

    #try catch block to catch if error is encountered, pass will return mars facts if passed
    try:
        browser.visit(url)
        html_string = browser.html
        soup = bs(html_string, 'lxml')

        keys =[]
        values=[]
        table = soup.find('table','tablepress tablepress-id-mars')
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            keys.append(columns[0].text)
            values.append(columns[1].text)
            facts = dict(zip(keys, values)) #facts in a dictionary as key-value pair
    except:
        pass
    return facts #facts in a dictionary as key-value pair

#Function to to obtain high resolution images for each of Mar's hemispheres
#5th scrape method declared 
def get_hemispheres(browser):
    hemisphere_image_urls = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 

    #try catch block to catch if error is encountered, pass will return Mar's hemispheres images
    try:
        browser.visit(url)     
        html_string = browser.html
        soup = bs(html_string, 'lxml')

        for header in soup.find_all("h3"):
            title = header.text
            uri = header.find_previous("a")
            image_url = 'https://astrogeology.usgs.gov'+ uri['href'] 
            browser.visit(image_url)

            sub_html_string = browser.html
            sub_soup = bs(sub_html_string, 'lxml')
            image_url='https://astrogeology.usgs.gov' + str(sub_soup.find('img','wide-image')['src'])
            hemisphere_image_urls.append({"title": title, "img_url": image_url})
            browser.back()
    except:
        pass
    return hemisphere_image_urls

#Function scrape to call the functions created to scrape various needed information from various website and consolidate it 
#it to output which is initialize as empty before.
def scrape():
    #call function to initialize Chrome Browser using Splinter
    browser = init_browser() 

    #empty object where all scrapre information will be stored in a k-v pair
    output = {}

    #call news scrape function - 1st scrape method
    news =get_news(browser)

    #call image URL scrape function - 2nd scrape method
    featured_image_url= get_featured_image(browser)

    #get latest weather update from Twitter - 3rd scrape method
    latest_weather=get_latest_weather(browser)

    #get Mars Facts information from Mars Facts webpage -4th scrape method
    facts =get_facts(browser)

    #Obtain high resolution images for each of Mar's hemispheres -5th declared scrape method
    hemisphere_image_urls =get_hemispheres(browser)

    #save all scrape information into output as key-value pair into a dictionary
    output ={ "news":news,"featured_image_url":featured_image_url,"weather":latest_weather,"facts":facts, "hemisphere_image_urls":hemisphere_image_urls}
    return output

