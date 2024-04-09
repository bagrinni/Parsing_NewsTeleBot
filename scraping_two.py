import requests
from bs4 import BeautifulSoup

def get_news_info(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    news_content = soup.find("div", class_="td-ss-main-content")
    if news_content:
        return news_content.get_text(strip=True)
    return "Новость не найдена."

def get_knews_articles(category):
    page_url = f"https://knews.kg/{category}/"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_titles = soup.find_all("h3", class_="entry-title td-module-title")
    
    for news_title in news_titles:
        title = news_title.get_text(strip=True)
        link = news_title.a["href"]
        yield {"title": title, "link": link}
