import pandas as pd
import os 
from src.student_Performance_p1 import logger 
from sklearn.linear_model import ElasticNet
import joblib
from src.student_Performance_p1.config.configuration import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def train_model(self):
        logger.info("Loading training data...")
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

# the elastic can only handel number for now so we just use this 
        logger.info("Splitting data into features and target...")
        x_train = train_data.drop(columns=[self.config.target_column,"ocean_proximity"] ,axis = 1)
        y_train = train_data[self.config.target_column]
        x_test = test_data.drop(columns=[self.config.target_column,"ocean_proximity"],axis = 1)
        y_test = test_data[self.config.target_column]
        logger.info("Splitting data into features and target...")


        logger.info("Training ElasticNet model...")
        model = ElasticNet(alpha=self.config.alpha, l1_ratio=self.config.l1_ratio, random_state=42)
        model.fit(x_train, y_train)

        logger.info("Saving trained model...")
        joblib.dump(model, self.config.model_name)