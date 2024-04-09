import requests
from bs4 import BeautifulSoup

def parse_weather():
    url = 'https://www.foreca.ru/Kyrgyzstan/Bishkek?details=20200521'
    response = requests.get(url)

    if response.status_code == 200:
        html_code = response.text
        soup = BeautifulSoup(html_code, 'html.parser')

        day_of_week = soup.find('div', class_='time').h2.text.strip()
        date = soup.find('div', class_='date').text.strip()
        weather = soup.find('div', class_='textual').p.span.text.strip()

        return f"День недели: {day_of_week}\nДата: {date}\nПрогноз: {weather}"
    else:
        return f'Ошибка при получении данных о погоде: {response.status_code}'
