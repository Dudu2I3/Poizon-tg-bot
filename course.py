# Импорт необходимых библиотек
import requests
from bs4 import BeautifulSoup

# URL для обменного курса юаня к рублю на Google
YUAN_RUB = ("https://www.google.com/search?q=%D1%8E%D0%B0%D0%BD%D0%B8+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D1%8F%D1%85&oq"
            "=%D1%8E%D0%B0%D0%BD%D0%B8+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D1%8F%D1%85&gs_lcrp"
            "=EgZjaHJvbWUyDwgAEEUYORiDARixAxiABDIHCAEQABiABDIHCAIQABiABDIICAMQABgWGB4yCAgEEAAYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yCAgHEAAYFhge0gEIMjg4MGoxajeoAgCwAgA&sourceid=chrome&ie=UTF-8")
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/17.0 Safari/605.1.15"}


def online_course():
    # Отправка запроса на страницу Google
    full_page = requests.get(YUAN_RUB, headers=headers)

    # Анализ HTML-кода с помощью BeautifulSoup
    soup = BeautifulSoup(full_page.content, "html.parser")

    # Поиск обменного курса на странице
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

    # Извлечение обменного курса и замена ',' на '.' для корректного преобразования в тип float
    convert = float(convert[0].text.replace(',', '.'))
    return convert
