import dill 
import numpy as np
import os
import pandas as pd
import psycopg2 as pg
import re
import sys 
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from TokyoRentML import databaseinfo
from TokyoRentML.exception import CustomException
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


class SaveTrainDataPostgresql:
    def __init__(self):
        database_info = databaseinfo.database_info
        logging.info("Save Train Data Initiated")
        self.connection_dict = {
            'host': database_info['host'],
            'dbname': database_info['dbname'],
            'user': database_info['user'],
            'password': database_info['pwd']
        }
        self.conn = None
        self.cur = None

    def connect(self):
        logging.info("Connect to train DataBase")
        self.conn = pg.connect(**self.connection_dict)
        self.cur = self.conn.cursor()
    
    def create_table(self):
        logging.info("Creating train Table")
        self.cur.execute("CREATE TABLE IF NOT EXISTS train\
                                (price BIGINT,\
                                size NUMERIC(6,2),\
                                deposit BIGINT,\
                                key_money BIGINT,\
                                year_built TEXT,\
                                unit_floor NUMERIC(4,1), \
                                total_floors NUMERIC(4,1), \
                                nearest_station_distance_in_min INT);")
        self.conn.commit()
    
    def insert_train_data(self, df: pd.DataFrame):
        logging.info("Inserting Data into train Table")
        query = """
            INSERT INTO train (price, size, deposit, key_money, year_built, unit_floor, total_floors, nearest_station_distance_in_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = [(row['price'], row['size'], row['deposit'], row['key_money'], row['year_built'], row['unit_floor'], row['total_floors'], row['nearest_station_distance_in_min']) for ind, row in df.iterrows()]
        self.cur.executemany(query, data)
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()


class ReadTrainData:
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
                price, size, deposit, key_money, year_built, unit_floor, total_floors, nearest_station_distance_in_min
                FROM train;
                """
        self.cur.execute(query)
        rows = self.cur.fetchall()

        data = pd.DataFrame(rows, columns=['price', 'size', 'deposit', 'key_money', 'year_built', 'unit_floor', 'total_floors', 'nearest_station_distance_in_min'])
        return data

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def read_data(self):
        self.connect()
        data = self.load_data()
        self.close_connection()
        return data


class SaveTestDataPostgresql:
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
        logging.info("Connect to test DataBase")
        self.conn = pg.connect(**self.connection_dict)
        self.cur = self.conn.cursor()
    
    def create_table(self):
        logging.info("Creating test Table")
        self.cur.execute("CREATE TABLE IF NOT EXISTS test\
                                (price BIGINT,\
                                size NUMERIC(6,2),\
                                deposit BIGINT,\
                                key_money BIGINT,\
                                year_built TEXT,\
                                unit_floor NUMERIC(4,1), \
                                total_floors NUMERIC(4,1), \
                                nearest_station_distance_in_min INT);")
        self.conn.commit()
    
    def insert_test_data(self, df: pd.DataFrame):
        logging.info("Inserting Data into test Table")
        query = """
            INSERT INTO test (price, size, deposit, key_money, year_built, unit_floor, total_floors, nearest_station_distance_in_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = [(row['price'], row['size'], row['deposit'], row['key_money'], row['year_built'], row['unit_floor'], row['total_floors'], row['nearest_station_distance_in_min']) for ind, row in df.iterrows()]
        self.cur.executemany(query, data)
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()


class ReadTestData:
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
                price, size, deposit, key_money, year_built, unit_floor, total_floors, nearest_station_distance_in_min
                FROM test;
                """
        self.cur.execute(query)
        rows = self.cur.fetchall()

        data = pd.DataFrame(rows, columns=['price', 'size', 'deposit', 'key_money', 'year_built', 'unit_floor', 'total_floors', 'nearest_station_distance_in_min'])
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


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file=file_path, mode="wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(x_train, y_train, x_test, y_test, models, params):
    try:
        report = {}
        fitters = {}
        for name, model in models.items():
            regr = model
            gs = GridSearchCV(regr, params[name], cv=3)
            gs.fit(x_train ,y_train)

            regr.set_params(**gs.best_params_)
            regr.fit(x_train ,y_train)
            
            y_test_pred = regr.predict(x_test)

            test_model_score = r2_score(y_test, y_test_pred)

            report[name] = test_model_score
            fitters[name] = regr
            logging.info(f"Model: {name} Uptimization is Done!")

        return report, fitters
    except Exception as e:
        raise CustomException(e, sys)
