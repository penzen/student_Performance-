from src.student_Performance_p1.config.configuration import ConfigurationManager, DataValidationConfig
from src.student_Performance_p1.components.data_validation import DataValidation
from src.student_Performance_p1 import logger
from student_Performance_p1.src.student_Performance_p1.components.data_transformation import DataTransformation
from student_Performance_p1.src.student_Performance_p1.pipelines.data_ingestion import STAGE_NAME
from student_Performance_p1.src.student_Performance_p1.pipelines.data_validation import DataValidationTrainingPipeline



STAGE_NAME = "Data Transformation Stage"


class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        config_manager = ConfigurationManager()
        data_transformation_config = config_manager.get_data_transformation_config()
        data_transformer = DataTransformation(config=data_transformation_config)
        data_transformer.initiate_data_transformation() # the train test split and save the data to the respective location


if __name__ == "__main__":
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataTransformationPipeline()
        obj.initiate_data_transformation()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(f"Error in data transformation stage: {e}")
        raise e
    