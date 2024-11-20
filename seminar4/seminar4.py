import requests
from lxml import html
import csv

"""Извлекаем данные про страну и ее население"""

countries = []
url = 'https://www.worldometers.info/world-population/population-by-country/'

# Получение содержимого страницы
try:
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})
    response.raise_for_status()  # проверка успешности запроса
except Exception as e:
    print(f'Ошибка при загрузке страницы: {e}!')
    exit()

try:
    tree = html.fromstring(response.content)
except Exception as e:
    print(f'Ошибка при парсинге страницы: {e}!')
    exit()

# Извлечение данных из таблицы
rows = tree.xpath('//tbody/tr')
for row in rows:
    try:
        country = row.xpath(".//td[2]//a/text()")[0] #используем относительный путь для поиска в текущей row
        population = int(row.xpath(".//td[3]/text()")[0].replace(',', ''))
        countries.append([country, population])
    except (IndexError, ValueError) as e:
        continue

#Запись в файл
with open('countries_population.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Country', 'Population'])
    writer.writerows(countries)
    print('Успешная запись в csv файл!')