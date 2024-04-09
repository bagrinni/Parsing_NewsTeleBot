import telebot
from telebot import types
from config import TOKEN, URL
from scraping import scrape_page, get_articles, get_article_info
from scraping_two import get_knews_articles,get_news_info
from weather import parse_weather
from database import  save_article_to_db

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_portal = types.KeyboardButton('24.kg')
    item_portal_two = types.KeyboardButton('K-News')
    item_portal_tree = types.KeyboardButton('Погода')
    markup.add(item_portal,item_portal_two, item_portal_tree)
    bot.send_message(message.chat.id, "Выберите новостной портал:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '24.kg')
def portal_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_vlast = types.KeyboardButton('Власть')
    item_tech = types.KeyboardButton('Техноблог')
    item_sport = types.KeyboardButton('Спорт')
    markup.add(item_vlast, item_tech, item_sport)
    bot.send_message(message.chat.id, "Выберите раздел новостей:", reply_markup=markup)
    


@bot.message_handler(func=lambda message: message.text == 'K-News')
def portal_menu_two(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_vlast = types.KeyboardButton('Политика')
    item_tech = types.KeyboardButton('Бизнес')
    item_sport = types.KeyboardButton('Проишествия')
    markup.add(item_vlast, item_tech, item_sport)
    bot.send_message(message.chat.id, "Выберите раздел новостей:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Погода')
def send_weather_info(message):
    weather_info = parse_weather()
    bot.send_message(message.chat.id, weather_info)
 

#_____________________________________________________________________________________________#
@bot.message_handler(func=lambda message: message.text == 'Власть')
def vlast(message):
    page_url = URL + '/vlast/'
    articles = scrape_page(page_url)
    articles_generator = get_articles(articles)
    message_generator = bot.send_message(message.chat.id, 'Loading...')

    try:
        article = next(articles_generator)
        bot.delete_message(message.chat.id, message_generator.message_id)  
        portal = '24.kg'  
        section = 'Власть'  
        save_article_to_db(message.chat.id, portal, section, article)
        send_article(message, article, articles_generator)
    except StopIteration:
        bot.delete_message(message.chat.id, message_generator.message_id)  
        bot.send_message(message.chat.id, 'На сегодня новости закончились.')

@bot.message_handler(func=lambda message: message.text == 'Техноблог')
def tech(message):
    page_url = URL + '/tehnoblog/'
    articles = scrape_page(page_url)
    articles_generator = get_articles(articles)
    message_generator = bot.send_message(message.chat.id, 'Loading...')

    try:
        article = next(articles_generator)
        bot.delete_message(message.chat.id, message_generator.message_id) 
        portal = '24.kg'  
        section = 'Техноблог'  
        save_article_to_db(message.chat.id, portal, section, article) 
        send_article(message, article, articles_generator)
    except StopIteration:
        bot.delete_message(message.chat.id, message_generator.message_id)  
        bot.send_message(message.chat.id, 'На сегодня новости закончились.')


@bot.message_handler(func=lambda message: message.text == 'Спорт')
def sport(message):
    page_url = URL + '/sport/'
    articles = scrape_page(page_url)
    articles_generator = get_articles(articles)
    message_generator = bot.send_message(message.chat.id, 'Loading...')

    try:
        article = next(articles_generator)
        bot.delete_message(message.chat.id, message_generator.message_id) 
        portal = '24.kg'  
        section = 'Спорт'  
        save_article_to_db(message.chat.id, portal, section, article) 
        send_article(message, article, articles_generator)
    except StopIteration:
        bot.delete_message(message.chat.id, message_generator.message_id)  
        bot.send_message(message.chat.id, 'На сегодня новости закончились.')

#_______________________________________________________________________________________________#

@bot.message_handler(func=lambda message: message.text == 'Политика')
def vlast_two(message):
    articles = get_knews_articles('vlast')
    send_articles_two(message, articles)
    


@bot.message_handler(func=lambda message: message.text == 'Бизнес')
def sport_buisnes(message):
    articles = get_knews_articles('business')
    send_articles_two(message, articles)



@bot.message_handler(func=lambda message: message.text == 'Проишествия')
def sport_buisnes(message):
    articles = get_knews_articles('action')
    send_articles_two(message, articles)

#___________________________________________________________________________________________________#

def send_articles_two(message, articles_generator):
    article = next(articles_generator, None)
    if article:
        send_article_two(message, article, articles_generator)
    else:
        bot.send_message(message.chat.id, "Новости не найдены.")



def send_article_two(message, article, articles_generator):
    article_title = article['title']
    article_link = article['link']
    
    bot.send_message(message.chat.id, f"Заголовок: {article_title}\nСсылка: {article_link}")

    news_info = get_news_info(article_link)

    if len(news_info) > 4096:
        chunks = [news_info[i:i+4096] for i in range(0, len(news_info), 4096)]
        for chunk in chunks:
            bot.send_message(message.chat.id, chunk)
    else:
        bot.send_message(message.chat.id, news_info)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_next = types.KeyboardButton('Далее')
    item_back = types.KeyboardButton('Назад к выбору раздела')
    item_back_to_portal = types.KeyboardButton('Назад к выбору портала')
    markup.add(item_next, item_back, item_back_to_portal)
    
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_next_step_two, articles_generator)


        
        


def send_article(message, article, articles_generator):
    message_parts = []
    message_parts.append(f'Заголовок: {article["title"]}\nСсылка: {article["link"]}')
    text_parts = article["text"].split('\n')
    for part in text_parts:
        if len(part) <= 4096:
            message_parts.append(part)
        else:
            message_parts.extend(split_message(part))
    
    bot.send_message(message.chat.id, message_parts[0])
    
    for part in message_parts[1:]:
        bot.send_message(message.chat.id, part)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_next = types.KeyboardButton('Далее')
    item_back = types.KeyboardButton('Назад к выбору раздела')
    item_back_to_portal = types.KeyboardButton('Назад к выбору портала')
    markup.add(item_next, item_back, item_back_to_portal)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_next_step, articles_generator)



def split_message(text, max_length=4096):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def handle_next_step(message, articles_generator):
    if message.text == 'Далее':
        try:
            article = next(articles_generator)
            send_article(message, article, articles_generator)
        except StopIteration:
            bot.send_message(message.chat.id, 'На сегодня новости закончились.')
    elif message.text == 'Назад к выбору раздела':
        portal_menu(message)
    elif message.text == 'Назад к выбору портала':
        start(message)


def handle_next_step_two(message, articles_generator):
    if message.text == 'Далее':
        try:
            article = next(articles_generator)
            send_article_two(message, article, articles_generator)
        except StopIteration:
            bot.send_message(message.chat.id, 'На сегодня новости закончились.')
    elif message.text == 'Назад к выбору раздела':
        portal_menu_two(message)
    elif message.text == 'Назад к выбору портала':
        start(message)











bot.polling()
