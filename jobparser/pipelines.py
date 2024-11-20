# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies201124

    def parse_salary(self, salary_list):

        if not salary_list:
            return 'Зарплата не указана'

        # объединяем список в строку и убираем лишние символы
        salary_str = ''.join(salary_list).replace('\xa0', '').strip()

        # определяем валюту
        currency = 'руб' if '₽' in salary_str else None

        # определяем тип зарплаты
        salary_type = None
        if 'на руки' in salary_str:
            salary_type = 'на руки'
        elif 'до вычета налогов' in salary_str:
            salary_type = 'до вычета налогов'

        if 'от' in salary_str and 'до' in salary_str:
            lower_bound = int(salary_str.split('от ')[1].split('до')[0].strip().replace(' ', ''))
            upper_bound = int(salary_str.split('до ')[1].split(' ')[0].strip().replace(' ', ''))
            return ['от', lower_bound, 'до', upper_bound, currency, salary_type] if salary_type else ['от', lower_bound,
                                                                                                      'до', upper_bound,
                                                                                                      currency]

        elif 'от' in salary_str:
            lower_bound = int(salary_str.split('от ')[1].split(' ')[0].strip().replace(' ', ''))
            return ['от', lower_bound, currency, salary_type] if salary_type else ['от', lower_bound, currency]


        elif 'до' in salary_str:
            upper_bound = int(salary_str.split('до ')[1].split(' ')[0].strip().replace(' ', ''))
            return ['до', upper_bound, currency, salary_type] if salary_type else ['до', upper_bound, currency]


    def process_item(self, item, spider):
        item['name'] = item.get('name')[0]
        item['salary'] = self.parse_salary(item.get('salary'))

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
