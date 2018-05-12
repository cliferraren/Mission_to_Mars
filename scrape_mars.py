import time
from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():
     # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "//Users/rck/chrome_driver/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    
def get_news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    try:
        browser.visit(url)
        html_string = browser.html
        soup = bs(html_string, 'html.parser')

        div = soup.find('div', attrs={'class': 'list_text'})
        title=div.findNext('div', {'class': 'content_title'}).text            
        description=div.findNext('div', {'class': 'article_teaser_body'}).text
    except:
        pass
    return {"news_title":title,"news_p":description}

def get_featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    try:
        browser.visit(url)
        button = browser.find_by_id("full_image")
        button.click()
        time.sleep(2)

        html_string = browser.html
        soup = bs(html_string, 'html.parser')
        anchor = soup.find('a','ready')
        if anchor.img:
            image_url = anchor.img['src']
        featured_image_url = "https://www.jpl.nasa.gov" + image_url      
    except:
        pass
    return featured_image_url

def get_latest_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    try:
        browser.visit(url)
        html_string = browser.html
        soup = bs(html_string, 'lxml')
        
        latest_weather = soup.find('div','js-tweet-text-container').text.strip()
    except:
        pass
    return latest_weather 

def get_facts(browser):
    url = 'https://space-facts.com/mars/'
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
            facts = dict(zip(keys, values))
    except:
        pass
    return facts

def get_hemispheres(browser):
    hemisphere_image_urls = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 
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

def scrape():
    browser = init_browser()
    output ={}
    news =get_news(browser)
    featured_image_url= get_featured_image(browser)
    latest_weather=get_latest_weather(browser)
    facts =get_facts(browser)
    hemisphere_image_urls =get_hemispheres(browser)
    output ={ "news":news,"featured_image_url":featured_image_url,"weather":latest_weather,"facts":facts, "hemisphere_image_urls":hemisphere_image_urls}
    return output
