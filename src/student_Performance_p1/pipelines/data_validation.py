from src.student_Performance_p1.config.configuration import ConfigurationManager, DataValidationConfig
from src.student_Performance_p1.components.data_validation import DataValidation
from src.student_Performance_p1 import logger
from student_Performance_p1.src.student_Performance_p1.pipelines.data_ingestion import STAGE_NAME

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config_manager = ConfigurationManager()
        data_validation_config = config_manager.get_data_validation_config()
        data_validator = DataValidation(config=data_validation_config)
        validation_result = data_validator.validate_all_columns()
        logger.info(f"Column validation result: {validation_result}")


if __name__ == "__main__":
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(f"Error in data validation stage: {e}")
        raise e
    