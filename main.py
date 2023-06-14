import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

SQLsystem = 'postgresql'
login = 'postgres'
password = '...'
host = 'localhost'
port = 5432
db_name = "publishers"
DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

if __name__ == '__main__':
    create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

def get_shops(publisher_info=None): #Функция принимает обязательный параметр
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop).join(
        Stock).join(Book).join(Publisher).join(Sale)
    if publisher_info.isdigit(): #Проверяем переданные данные в функцию на то, что строка состоит только из чисел
        items = q.filter(Publisher.id == int(publisher_info)).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где айди публициста равно переданным данным в функцию, и сохраняем в переменную
    else:
        items = q.filter(Publisher.name == str(publisher_info)).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где имя публициста равно переданным данным в функцию, и сохраняем в переменную
    for b, s, p, d in items: #При каждой итерации получаем кортеж и распаковываем значения в 4 переменные
        print(f"{b: <40} | {s: <10} | {p: <8} | {d.strftime('%d-%m-%Y')}") #Передаем в форматированную строку переменные, которые содержат имя книги, название магазина, стоимость продажи и дату продажи


if __name__ == '__main__':
    publisher_info = (input("Введите название или ID издательства: ")).capitalize() #Просим клиента ввести имя или айди публициста и данные сохраняем в переменную
    get_shops(publisher_info) #Вызываем функцию получения данных из базы, передавая в функцию данные, которые ввел пользователь строкой выше
session.close()
