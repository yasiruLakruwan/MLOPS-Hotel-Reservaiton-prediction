from src.logger import get_logger
from src.custom_exeption import CustomExeption
import pandas as pd
import numpy as np
from google.cloud import storage
from sklearn.model_selection import train_test_split
from config.path_config import *
from utils.common_functions import read_yaml
import sys

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]


        os.makedirs(raw_dir,exist_ok=True)

        logger.info(f"Data ingestion started with {self.bucket_name} and file {self.file_name}")

    def download_csv_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)


            blob.download_to_filename(raw_file_path)

            logger.info(f"CSV file is successfully downloaded to {raw_file_path}")
        
        except Exception as e:
            logger.error("error while downloading the datafile")
            raise CustomExeption("failed to download csv file",e)
    
    def split_data(self):
        try:
            logger.info("starting spliting data")
            data = pd.read_csv(raw_file_path)

            train_data,test_data =  train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)

            train_data.to_csv(train_file_path)
            test_data.to_csv(test_file_path)

            logger.info("Train data saved.")
            logger.info("Test data saved. ")

        except Exception as e:
            logger.error("error while spliting data")
            raise CustomExeption("failed to make train and test data",e)
        
    def run(self):
        try:
            logger.info("Starting data ingesting process")
            self.download_csv_gcp()
            self.split_data()

            logger.info("data ingestion done successfully")

        except CustomExeption as e:
            logger.error(f"CustomExeption : {str(e)}")
        
        finally:
            logger.info("Data ingestion complete")


if __name__ == "__main__":
    dataingestion = DataIngestion(read_yaml(config_file_path))
    dataingestion.run()