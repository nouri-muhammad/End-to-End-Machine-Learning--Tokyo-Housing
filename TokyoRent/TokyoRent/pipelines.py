# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2 as pg
from itemadapter import ItemAdapter
from . import databaseinfo


class TokyorentPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'price':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][1:]
            elif field_name == 'size':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][:-3]
            elif field_name == 'deposite':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][1:]
            elif field_name == 'key_money':
                value = adapter.get(field_name)
                adapter[field_name] = value[0][1:]
            elif field_name == 'floor':
                value = adapter.get(field_name)
                if value[0]:
                    value = value[0]
                    first = value[:value.index('/')].strip()
                    second = value[value.index('/')+2:-1]
                    adapter[field_name] = f"{first},{second}"
                else:
                    adapter[field_name] = '' 
        
        return item



"""
create a databaseinfo.py file in this file's directory to extract the information of your database from.
Fill the created file as followed:
database_info = {
    'host': 'enter the host ip of your postgres',
    'dbname': 'enter your prepared database name',
    'user': 'enter your user name',
    'pwd': 'enter your password',
}
"""


class SavePostgresqlPipeline:
    def __init__(self):
        database_info = databaseinfo.database_info

        self.connection_dict = {
            'host': database_info['host'],
            'dbname': database_info['dbname'],
            'user': database_info['user'],
            'password': database_info['pwd']
        }
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = pg.connect(**self.connection_dict)
        self.cur = self.conn.cursor()
    
    def create_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS rent\
                                (detail TEXT,\
                                price TEXT,\
                                size TEXT,\
                                deposite TEXT,\
                                key_money TEXT,\
                                floor TEXT, \
                                year_built TEXT,\
                                nearest_station TEXT);")
        self.conn.commit()
    
    def insert_rent_data(self, item, spider ):
        query = """
            INSERT INTO rent (detail, price, size, deposite, key_money, floor, year_built, nearest_station)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = (item['detail'], item['price'], item['size'], item['deposite'], item['key_money'], item['floor'], item['year_built'], item['nearest_station'])
        self.cur.execute(query, data)
        self.conn.commit()
        return item

    def close_connection(self, spider):
        self.cur.close()
        self.conn.close()

    def open_spider(self, spider):
        self.connect()
        self.create_table()

    def process_item(self, item, spider):
        return self.insert_rent_data(item, spider)

    def spider_closed(self, spider):
        self.close_connection(spider)
