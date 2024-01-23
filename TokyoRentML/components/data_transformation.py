import numpy as np 
import os 
import sys
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline 
from TokyoRentML.exception import CustomException
from TokyoRentML.logger import logging
from TokyoRentML.utils import (
    ReadTrainData,
    ReadTestData,
    save_object
)


class DataTransformation:

    def __init__(self):
        self.train_df = ReadTrainData()
        self.test_df = ReadTestData()
    
    def get_data_transformer_obj(self):
        try:
            numerical_cols = ['size', 'deposit', 'key_money', 'year_built', 'unit_floor', 'total_floors', 'nearest_station_distance_in_min']

            num_pipeline = Pipeline(
                steps=[
                    ("Scaler", StandardScaler())
                ]
            )
            logging.info("Numerical Columns' Scaling Completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_cols),
                ]
            )
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("Getting Preprocessor Object")
            preprocessor_obj = self.get_data_transformer_obj()

            target_col_name = 'price'

            logging.info("Reading Train and Test Data")
            train_df = self.train_df.read_data()
            test_df = self.test_df.read_data()

            logging.info("Split Train and Test Data into Feature and Target")
            input_feature_train_df = train_df.drop(columns=[target_col_name], axis=1)
            target_feature_train_df = train_df[target_col_name]

            input_feature_test_df = test_df.drop(columns=[target_col_name], axis=1)
            target_feature_test_df = test_df[target_col_name]
            
            logging.info("Apply Preprocessing Object on Train and Test Data")
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            logging.info("Create Train and Test Arrays")
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            
            logging.info("Save Preprocessing Object")
            preprocessor_obj_file_path = os.path.join('processed_data', 'preprocessor.pkl')
            save_object(
                file_path=preprocessor_obj_file_path,
                obj=preprocessor_obj
            )
            print(preprocessor_obj_file_path)

            return(
                train_arr, 
                test_arr, 
                preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
