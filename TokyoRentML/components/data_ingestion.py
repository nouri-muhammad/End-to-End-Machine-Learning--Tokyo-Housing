import os
import pandas as pd 
import sys
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from TokyoRentML.exception import CustomException
from TokyoRentML.logger import logging
from TokyoRentML.utils import (
    ReadPostgresDataBase, 
    remove_after_white_space, 
    remove_comma, 
    floor_to_tuple, 
    station_cleaning,
    extract_detail,
    split_floor_column
)


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('processed_data', 'train.csv')
    test_data_path: str = os.path.join('processed_data', 'test.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Initiate Data Ingestion")
        try:
            df = ReadPostgresDataBase()
            logging.info("Reading Data from Database")
            df = df.read_data()

            logging.info("Dropping Rows With Null Values")
            df.dropna(inplace=True)

            logging.info("Clearing price Column")
            df['price'] = df['price'].apply(remove_comma)
            df['price'] = df['price'].apply(remove_after_white_space)
            df['price'] = df['price'].astype('int')

            logging.info("Cleaning size Column")
            df['size'] = df['size'].astype('float')

            logging.info("Clean deposit Column")
            df['deposit'] = df['deposit'].apply(remove_comma)
            df['deposit'] = df['deposit'].astype('int')

            logging.info("Clean key_money Column")
            df['key_money'] = df['key_money'].apply(remove_comma)
            df['key_money'] = df['key_money'].astype('int')

            logging.info("Clean year_built Column")
            df['year_built'] = df['year_built'].astype('int')

            logging.info("Clean floor Column")
            df['floor'] = df['floor'].apply(floor_to_tuple)
            df = split_floor_column(df)

            logging.info("Clean nearest_station Column")
            df['nearest_station_distance_in_min'] = df['nearest_station'].apply(station_cleaning)
            df['nearest_station_distance_in_min'] = df['nearest_station_distance_in_min'].astype('int')
            df.drop(columns=['nearest_station'], axis=1, inplace=True)

            logging.info("Clean detail Column")
            df['detail'] = df['detail'].apply(extract_detail)

            logging.info("Dropping Rows With Null Values")
            df.dropna(inplace=True)

            return df

        except Exception as e:
            raise CustomException(e, sys) 


if __name__=='__main__':
    obj = DataIngestion()
    data = obj.initiate_data_ingestion()


