import os
import pandas as pd
import numpy as np
from config.path_config import PROCESSED_DATA_TEST_PATH, PROCESSED_DATA_TRAIN_PATH,config_file_path,train_file_path,test_file_path,PROCESSED_DIR,raw_file_path,raw_dir
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
            df.drop(columns=['Unnamed: 0', 'Booking_ID'],inplace=True)
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

            for column in skewness[skewness>skewness_threshold].index:
                df[column] = np.log1p(df[column])
            return df

        except Exception as e:
            logger.error("Error during data processing step {e}")
            raise CustomExeption("Error while preprocess data",e)
        
    def balance_data(self,df):
        try:
            logger.info("Starting data processing")

            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            smote = SMOTE(random_state=42)

            X_resumpled , y_resumpled = smote.fit_resample(X,y)

            balanced_df = pd.DataFrame(X_resumpled , columns=X.columns)
            balanced_df["booking_status"] = y_resumpled

            logger.info("Completed balancing data")
            return balanced_df
        

        except Exception as e:
            logger.error("Error during data balancing step {e}")
            raise CustomExeption("Error while balancing data",e)
        
    def select_features(self,df):
        try:
            logger.info("Starting the feature selection step")

            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                            'feature':X.columns,
                            'importance':feature_importance
                        })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            no_of_features = self.config["data_processing"]["no_of_features"]

            top_10_features = top_features_importance_df["feature"].head(no_of_features).values

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature selected successfully")

            return top_10_df

        except Exception as e:
            logger.error("Error during feature selection step {e}")
            raise CustomExeption("Error while feature selection data",e)
        
    def save_data(self,df, file_path):
        try:
            logger.info("Saving processed data to the processed folder.")
            df.to_csv(file_path, index = False)
            logger.info(f"Successfully saved data to the folder {file_path}")
        except Exception as e:
            logger.error("Error during feature selection step {e}")
            raise CustomExeption("Error while feature selection data",e)
    
    # Now combined the all functions and process data.

    def process(self):
        try:
            logger.info("Loading data from the RAW direcry")

            train_df = read_csv(self.train_path)
            test_df = read_csv(self.test_path)

            train_df = self.process_data(train_df)
            test_df = self.process_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df,PROCESSED_DATA_TRAIN_PATH)
            self.save_data(test_df, PROCESSED_DATA_TEST_PATH)

            logger.info("Data preprocessing complete in combined functions")

        except Exception as e:
            logger.error("Error happening combined process step.")
            CustomExeption("Error while in the combined process step",e)

if __name__ == "__main__":
    processor = DataProcessor(train_file_path,test_file_path,PROCESSED_DIR,config_file_path)
    processor.process()