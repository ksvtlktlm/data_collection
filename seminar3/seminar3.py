import json
from pymongo import MongoClient
from pprint import pprint


client = MongoClient('mongodb://localhost:27017/')
db = client['book_database'] #создание б/д
collection = db['books'] #создание коллекции в б/д

with open('my_books.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for book in data:
    collection.update_one({"Name": book.get("Name")}, {"$set": book}, upsert=True)

print('100 книг с сортировкой по названию:\n')
for book in collection.find().sort("Name", 1).limit(100):
    pprint(book)
print()

print('Книги дороже 12 и дешевле 13 евро:\n')
for book in collection.find({"Price, euro": {"$gt": 12, "$lt": 13}}):
    pprint(book)
print()

print('Книги, количество которых в наличии больше 20:\n')
for book in collection.find({"In_stock": {"$gt": 20}}):
    pprint(book)
print()

print('Названия книг, в описании которых есть слово love:\n')
for book in collection.find({"Description": {"$regex": "love", "$options": "i"}}, {"Name": 1, "_id": 0}): #не чувствительный к регистру поиск
    print(book)
print()

print('Названия книг дешевле 11 евро с рейтингом 5:\n')
for book in collection.find({"Price, euro": {"$lte": 11}, "Rate": 5}, {"Name": 1, "_id": 0}):
    pprint(book)
print()