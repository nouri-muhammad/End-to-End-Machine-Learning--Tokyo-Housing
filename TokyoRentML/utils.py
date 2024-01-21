import pandas as pd
import psycopg2 as pg
from TokyoRentML import databaseinfo
from TokyoRentML.logger import logging



class ReadPostgresDataBase:
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

    def load_data(self):
        query = """ SELECT 
                detail, price, size, deposite, key_money, floor, year_built, nearest_station
                FROM rent;
                """
        self.cur.execute(query)
        rows = self.cur.fetchall()

        data = pd.DataFrame(rows, columns=['detail', 'price', 'size', 'deposit', 'key_money', 'floor', 'year_built', 'nearest_station'])
        return data

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def read_data(self):
        self.connect()
        data = self.load_data()
        self.close_connection()
        return data

        
