import psycopg2


def create_articles_table():
    conn = psycopg2.connect("dbname=newsbot user=botnews password=2569 host=localhost")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articless (
        id SERIAL PRIMARY KEY,
        portal TEXT,
        section TEXT,
        title TEXT,
        link TEXT UNIQUE,
        text TEXT
    );
    ''')
    conn.commit()

def save_article_to_db(chat_id, portal, section, article_info):
    conn = psycopg2.connect("dbname=newsbot user=botnews password=2569 host=localhost")

    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO articlesss (chat_id, portal, section, title, link, text) 
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', (chat_id, portal, section, article_info['title'], article_info['link'], article_info['text']))
    conn.commit()
    cursor.close()
    conn.close()
