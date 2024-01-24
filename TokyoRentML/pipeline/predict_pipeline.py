import pandas as pd 
import sys
from TokyoRentML.exception import CustomException
from TokyoRentML.utils import load_object


class PreditPipeline:
    def __init__(self) -> None:
        pass

    def predict(self, features):
        try:
            model_path = 'processed_data/model.pkl'
            preprocessor_path = 'processed_data/preprocessor.pkl'
            model = load_object(model_path)
            preprocessor = load_object(preprocessor_path)
            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            return pred 
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(
            self,
            size,
            deposit,
            key_money,
            year_built,
            unit_floor,
            total_floors,
            nearest_station_distance_in_min
    ):
        self.size = size
        self.deposit = deposit
        self.key_money = key_money
        self.year_built = year_built
        self.unit_floor = unit_floor
        self.total_floors = total_floors
        self.nearest_station_distance_in_min = nearest_station_distance_in_min

    def get_data_as_df(self):
        try:
            custom_data_input = {
                'size': [self.size],
                'deposit': [self.deposit],
                'key_money': [self.key_money],
                'year_built': [self.year_built],
                'unit_floor': [self.unit_floor],
                'total_floors': [self.total_floors],
                'nearest_station_distance_in_min': [self.nearest_station_distance_in_min]
            }
            return pd.DataFrame(custom_data_input)
        except Exception as e:
            raise CustomException(e, sys) 
