
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import re


def mars_news(browser):
    print("Scraping Mars News")
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Image

def featured_image(browser):
    print("Scraping featured image")
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    print("Scraping Mars facts")
    # Add try/except for error handling
    # try:
    #     # Use 'read_html' to scrape the facts table into a dataframe
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    #     print(df.head())
    # except BaseException:
    #     return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def hemispheres(browser):
    print("Scraping Mars hemispheres")
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    img_soup = soup(html, 'html.parser')

    number_results = img_soup.find('span', class_='count').get_text()
    results_count_list = re.findall(r'\d+', number_results)
    results_count = int(results_count_list[0])
    hemisphere_image_urls = []
    for i in range(results_count):
        hemisphere_results = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.find_by_text('Sample').first
        img_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemisphere_results["img_url"] = img_url
        hemisphere_results["title"] = title
        hemisphere_image_urls.append(hemisphere_results)
        browser.back()

    return hemisphere_image_urls


def scrape_all():
    print("Beginning Scrape all function")
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemispheres(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
