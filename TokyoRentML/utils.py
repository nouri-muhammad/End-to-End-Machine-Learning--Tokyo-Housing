import numpy as np
import pandas as pd
import psycopg2 as pg
import re
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


def remove_after_white_space(x):
    if ' ' in x:
        return x.split(' ')[0]
    else:
        return x


def remove_comma(x):
    return x.replace(',', '')


def floor_to_tuple(x):
    return tuple(map(str, x.split(',')))


def split_floor_column(df):
    # Create new columns for the first and second elements of the tuple

    df['unit_floor'] = np.nan
    df['total_floors'] = np.nan
    for i, row in df.iterrows():
        try:
            if row['floor'][0]:
                df.at[i, 'unit_floor'] = float(row['floor'][0])
            else:
                df.at[i, 'unit_floor'] = None
            if row['floor'][1]:
                df.at[i, 'total_floors'] = float(row['floor'][1])
            else:
                df.at[i, 'total_floors'] = None
        except IndexError:
            pass

    # Drop the original 'floor' column
    df = df.drop('floor', axis=1)
    return df


def station_cleaning(x):
    # search for the word "min" in the value
    minutes = re.findall(r'(\d+)\s*min', x)
    return sum(int(m) for m in minutes)


def extract_detail(x):
    """
    from details column only the middle part of the address might be usefull in large amount of data.
    The last part is the city of Tokyo which is the city and same for all the data, so there is no use in it.
    The first part is the exact location of the apartment, and there are too many unique values thus
        it will be almost unique for each entery and is of no use.
    The second part is the only part that is of use which is the broader location. 
    """
    # Extract the second part between commas
    second_part = re.search(r',\s*"(.*?),', x).group(1)    
    # Return second part
    return second_part


