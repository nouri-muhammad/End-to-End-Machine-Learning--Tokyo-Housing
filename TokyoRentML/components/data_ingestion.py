import os
import pandas as pd 
import sys
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from TokyoRentML.exception import CustomException
from TokyoRentML.logger import logging
from TokyoRentML.utils import ReadPostgresDataBase


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
            print(df)
        except Exception as e:
            raise CustomException(e, sys) 


if __name__=='__main__':
    obj = DataIngestion()
    obj.initiate_data_ingestion()