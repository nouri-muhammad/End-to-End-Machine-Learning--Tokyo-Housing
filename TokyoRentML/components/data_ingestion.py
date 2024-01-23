import sys
from sklearn.model_selection import train_test_split
from TokyoRentML.components.data_transformation import DataTransformation
from TokyoRentML.exception import CustomException
from TokyoRentML.logger import logging
from TokyoRentML.components.model_trainer import ModelTrainer
from TokyoRentML.utils import (
    ReadPostgresDataBase, 
    remove_after_white_space, 
    remove_comma, 
    floor_to_tuple, 
    station_cleaning,
    split_floor_column,
    SaveTrainDataPostgresql,
    SaveTestDataPostgresql
)


class DataIngestion:
    def __init__(self):
        self.df_obj = ReadPostgresDataBase()

    def initiate_data_ingestion(self):
        try:
            logging.info("Reading Data from Database")
            df = self.df_obj.read_data()

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

            logging.info("Drop detail Column")
            df.drop(columns=['detail'], axis=1, inplace=True)

            logging.info("Dropping Rows With Null Values")
            df.dropna(inplace=True)

            # save both train and test data in postgresql
            logging.info("Train Test Split Initiated")
            train_set, test_set =  train_test_split(df, test_size=0.2, random_state=91)

            logging.info("Save Train Data in Postgres")
            train = SaveTrainDataPostgresql()
            train.connect()
            train.create_table()
            train.insert_train_data(train_set)
            train.close_connection()

            logging.info("Save Test Data in Postgres")
            test = SaveTestDataPostgresql()
            test.connect()
            test.create_table()
            test.insert_test_data(test_set)
            test.close_connection()

            logging.info("Ingestion Process Completed")

        except Exception as e:
            raise CustomException(e, sys) 


if __name__=='__main__':
    obj = DataIngestion()
    obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_array, test_array, preprocessor_obj_file_path = data_transformation.initiate_data_transformation()

    model_trainer = ModelTrainer()
    result = model_trainer.initiate_model_trainer(train_array, test_array)
