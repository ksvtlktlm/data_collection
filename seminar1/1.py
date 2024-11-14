import requests
import json
import os
from dotenv import load_dotenv
from pprint import pprint

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


city = input("Введите название города: ")
category = input("Введите категорию заведения: ")
print()

url = "https://api.foursquare.com/v3/places/search?sort=RATING"

headers = {
    "accept": "application/json",
    "Authorization": os.getenv('API_KEY')
}

params = {
    "near": city,
    "limit": 15,
    "query": category
}
response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    data = json.loads(response.text)
    places = data["results"]
    for place in places:
        print("Название:", place["name"])
        print("Адрес:", place["location"]["formatted_address"])
        print("Рейтинг: не обнаружен в выдаче сервера")
        print()
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    pprint(response.text)
