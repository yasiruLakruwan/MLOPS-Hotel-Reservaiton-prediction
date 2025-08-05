## This file uses to create the common functions uses in the project
## In this file uses to 

import os 
import pandas
from src.logger import get_logger
from src.custom_exeption import CustomExeption
import yaml
import pandas as pd

# function to read yaml file.
logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in given path")
        with open(file_path,'r') as file:
            config = yaml.safe_load(file)
            logger.info("Successfully load the yaml file.") 
            return config

    except CustomExeption as e:
        logger.error("Error while loading the yaml file")
        raise CustomExeption("Falil to read the yaml file",e)

# function to read csv files

def read_csv(path):
    try:
        logger.info("Reading CSV file")
        return pd.read_csv(path)
    except Exception as e:
        logger.error("Error happening when reading the csv file {e}")
        raise CustomExeption("CSV reading error",e)
    