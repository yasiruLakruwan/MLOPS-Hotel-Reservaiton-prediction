import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exeption import CustomExeption
from config import *
from utils.common_functions import read_yaml,read_csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# lets perform preprocessing

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config= read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def process_data(self,df):
        try:
            logger.info("Starting our Data Preprocessing step")
            logger.info("Droping the columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'])
            df.drop_duplicates(inplace = True)

            cat_col = self.config["data_processing"]["categorical_columns"]
            num_col = self.config["data_processing"]["neumarical_columns"]

            label_encoder = LabelEncoder()

            mappings={}

            for col in cat_col:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}
            logger.info("Lable mappings are: ")

            for col,mapping in mappings.items():
                logger.info(f"{col}:{mapping}")

            logger.info("Doing skewness haandling")

            skewness_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_col].apply(lambda x:x.skew())

        except:
            pass