import os
import pandas as pd
import numpy as np
import joblib
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from logger import get_logger
from src.custom_exeption import CustomExeption
from config.path_config import *
from config.model_params import *
from utils.common_functions import read_csv

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self,trian_path,test_path,model_output_path):
        self.train_path = trian_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Load train data from {self.train_path}")
            train_df = read_csv(self.train_path)
            logger.info(f"Load test data from {self.test_path}")
            test_df = read_csv(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data splitted successfully for model training")

            return X_train,y_train,X_test,y_test

        except Exception as e:
            logger.error(f"Error hapening while loading data {e}")
            raise CustomExeption("Failed to split the data",e)

    def train_lgbm(self,X_train,y_train):
        try:
            logger.info("Start training the model")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting our hyperparameter tuning")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
            )
            logger.info("Starting out model training")

            random_search.fit_(X_train,y_train)

            logger.info("Hyperparameter tuning completed. ")


            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters are {best_params}")

            return best_lgbm_model
         
        except Exception as e:
            logger.error(f"Error while tranin model {e}")
            raise CustomExeption("Error while training the model",e)
    
    def evaluate_model(self,model,X_test,y_test):
        try:
            logger.info("Logging evaluating")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy score: {accuracy}")
            logger.info(f"Precision score: {precision}")
            logger.info(f"Recall score: {recall}")
            logger.info(f"F1 score: {f1}")

            return {
                "accuracy": accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1": f1
            }
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomExeption("Fail to evaluate model",e)
        

    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)
            logger.info("Saving the model")
            joblib.dump(model,self.model_output_path)
            logger.info(f"Model save to {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error hapening saving the model {e}")
            raise CustomExeption("Failed during saving the model",e)
        
    def run(self):
        try:
            logger.info("Srarting our model pipeline")

            X_train,y_train,X_test,y_test = self.load_and_split_data()
            best_lgbm_model = self.train_lgbm(X_train,y_train)
            metrics = self.evaluate_model(best_lgbm_model,X_test,y_test)
            self.save_model(best_lgbm_model)

            logger.info("Model training successfully completed")
        except Exception as e:
            logger.error(f"Error happening while combined method running {e}")
            raise CustomExeption("Failed to train the model.")