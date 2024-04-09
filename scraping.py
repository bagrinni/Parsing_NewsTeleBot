import requests
from bs4 import BeautifulSoup as Bs
from config import URL


def scrape_page(page_url):
    r = requests.get(page_url)
    s = Bs(r.text, 'html.parser')
    articles = s.find_all('div', class_='one')
    return articles

def get_article_info(article_url):
    article_r = requests.get(article_url)
    article_s = Bs(article_r.text, 'html.parser')
    
    title = article_s.find('h1', class_='newsTitle').get_text(strip=True)
    article_text = article_s.find('div', class_='cont').get_text(strip=True)
    
    article_info = {
        'title': title,
        'link': article_url,
        'text': article_text
    }
    
    return article_info


def get_articles(articles):
    for article in articles:
        link = article.find('a').get('href')
        if link:
            article_url = URL + link
            yield get_article_info(article_url)




