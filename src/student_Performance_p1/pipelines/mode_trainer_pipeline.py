from src.student_Performance_p1.config.configuration import ConfigurationManager, DataValidationConfig
from src.student_Performance_p1.components.model_trainer import ModelTrainerConfig
from src.student_Performance_p1 import logger
from student_Performance_p1.src.student_Performance_p1.pipelines.data_ingestion import STAGE_NAME




STAGE_NAME = "Model training name"


class ModelTrainerPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config_manager = ConfigurationManager()
        model_trainer_config = config_manager.get_model_trainer_config()
        model_trainer_config = ModelTrainerConfig(config_manager = model_trainer_config)
        model_trainer_config.train()

