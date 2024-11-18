
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from urllib.parse import urljoin
import json
import time
from tqdm import tqdm


start = time.time()
result_json = []
base_url = 'http://books.toscrape.com/'
count = 0

ratings = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4,'Five': 5}



def get_soup(html):
    try:
        response = session.get(html, headers={"user-agent": UserAgent().random})
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except requests.RequestException as e:
        print(f'Произошла ошибка при загрузке страницы {html}: {str(e)}')


def get_data(soup):
    try:
        features = soup.find('div', 'col-sm-6 product_main')
        name = features.find('h1').text if features.find('h1') else None
        price = float(features.find('p', 'price_color').text[1:]) if features.find('p', 'price_color') else None
        in_stock = int(
            ''.join(filter(str.isdigit, features.find('p', 'instock availability').text))) if features.find('p',
                                                                                                            'instock availability') else None
        rating = ratings.get(soup.find('p', class_='star-rating').get('class')[1]) if soup.find('p',
                                                                                             class_='star-rating') else None
        description = soup.find('div', id='product_description').find_next('p').text if soup.find('div', id='product_description') and soup.find('div', id='product_description').find_next('p') else None
        return name, price, rating, in_stock, description
    except Exception as e:
        print(f"Ошибка при извлечении данных: {e}")
        return None, None, None, None, None

def res_json_append(data):
    result_json.append({'Name': data[0],
                        'Price, euro': data[1],
                        'Rate': data[2],
                        'In_stock': data[3],
                        'Description': data[4]})


with requests.Session() as session:
    source_page = get_soup('http://books.toscrape.com/')
    if not source_page:
        print("Не удалось загрузить основную страницу.")
        exit()
    relative_links_categories = [el.get('href') for el in source_page.find('div', 'side_categories').find_all('a')]
    for relative_link in tqdm(relative_links_categories[1:], desc="ЗАГРУЖЕНО КАТЕГОРИЙ"):
        full_link_category = urljoin(base_url, relative_link)
        soup_category = get_soup(full_link_category)
        print(f'\nСобираем категорию {full_link_category.split("/")[-2].split('_')[0]}...')

        link_books = ['/'.join(el.find('a').get('href').split('/')[-2:]) for el in
                      soup_category.find_all('article', 'product_pod')]
        for relative_link_book in link_books:
            full_link_book = base_url + 'catalogue/' + relative_link_book
            soup_book = get_soup(full_link_book)
            features_book = get_data(soup_book)
            res_json_append(features_book)
            count += 1


        pager = soup_category.find('ul', 'pager')
        while True:
            if pager and pager.find('li', 'next'):
                next_relative_link = pager.find('li', 'next').find('a').get('href')
                full_link = '/'.join(full_link_category.split('/')[:-1]) + '/' + next_relative_link
                print('Переходим на следующую страницу текущей категории...')
                next_soup = get_soup(full_link)
                link_books = ['/'.join(el.find('a').get('href').split('/')[-2:]) for el in
                              next_soup.find_all('article', 'product_pod')]
                for relative_link_book in link_books:
                    full_link_book = base_url + 'catalogue/' + relative_link_book
                    soup_book = get_soup(full_link_book)
                    features_book = get_data(soup_book)
                    res_json_append(features_book)
                    count +=1
                pager = next_soup.find('ul', 'pager')
            else:
                break

with open('my_books.json', 'w', encoding='utf-8') as file:
    json.dump(result_json, file, indent=4, ensure_ascii=False)
    print('Файл успешно записан!')
print(f'Добавлено {count} записей.')
print(f'Время выполнения: {time.time() - start}') #получилось многовато. потом попробую переписать асинхронно
