import os 
from src.student_Performance_p1 import logger
from sklearn.model_selection import train_test_split
import pandas as pd

from student_Performance_p1.src.student_Performance_p1.entity.config_entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def initiate_data_transformation(self):
        logger.info("Reading the data from the source")
        df = pd.read_csv(self.config.data_path)

        logger.info("Splitting the data into train and test sets")
        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

        logger.info("Saving the train and test sets to the specified paths")
        train_set.to_csv(self.config.train_data_path, index=False)
        test_set.to_csv(self.config.test_data_path, index=False)

        logger.info(f"Train data saved at: {self.config.train_data_path}")
        logger.info(f"Test data saved at: {self.config.test_data_path}")