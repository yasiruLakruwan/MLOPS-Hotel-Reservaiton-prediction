from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.path_config import *

if __name__ == "__main__":
    # Data ingestion pipeline  

    dataingestion = DataIngestion(read_yaml(config_file_path))
    dataingestion.run()

    # Data Processing pipeline  

    processor = DataProcessor(train_file_path,test_file_path,PROCESSED_DIR,config_file_path)
    processor.process()

    # Model Training pipeline

    trainer = ModelTraining(PROCESSED_DATA_TRAIN_PATH,PROCESSED_DATA_TEST_PATH,MODEL_OUTPUT_PATH)
    trainer.run()
