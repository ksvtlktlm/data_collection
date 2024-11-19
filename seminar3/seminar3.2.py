import json
from clickhouse_driver import Client


client = Client('localhost')
client.execute('CREATE DATABASE IF NOT EXISTS books_db')
client.execute('USE books_db')


client.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id UInt64,
        Name String,
        Price String,
        In_stock UInt32,
        Price, euro UInt32, 
        Description String, 
        Rate UInt32
    ) ENGINE = MergeTree()
    ORDER BY id
''')


with open('my_books.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


for book in data:
    client.execute('INSERT INTO books (Name, Price, Rate, In_stock, Description) VALUES', [
        (book.get('Name', ''),
         float(book.get('Price, euro', 0)),
         int(book.get('Rate', 0)),
         int(book.get('In_stock', 0)),
         book.get('Description', ''))
    ])

print("Данные успешно загружены в ClickHouse.")


# Получение всех записей
rows = client.execute('SELECT * FROM books')
print("Все книги:")
for row in rows:
    print(row)

# Книги дороже 5 евро
rows = client.execute('SELECT Name, Price FROM books WHERE Price > 5')
print("Книги дороже 5 евро:")
for row in rows:
    print(row)
