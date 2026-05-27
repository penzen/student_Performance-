
from src.student_Performance_p1.config.configuration import ConfigurationManager
from src.student_Performance_p1.components.data_ingestion import DataIngestor
from src.student_Performance_p1.components.data_validation import DataValidation
from src.student_Performance_p1.pipelines.mode_trainer_pipeline import ModelTrainerPipeline


class DataIngestionPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingest_config()

        data_ingestion = DataIngestor(config=data_ingestion_config)
        data_ingestion.download_data()
        data_ingestion.unzip_data()



STAGE_NAME = "Data Ingestion Stage"


try:
    print(f">>>>> stage {STAGE_NAME} started <<<<<")
    obj = DataIngestionPipeline()
    obj.initiate_data_ingestion()
    print(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
except Exception as e:
    print(e)
    raise e


STAGE_NAME = "Data Validation Stage"
try:
    print(f">>>>> stage {STAGE_NAME} started <<<<<")
    data_validation_config =  DataIngestionPipeline()
    data_validation_config.initiate_data_ingestion()
except Exception as e:
    raise e

STAGE_NAME = "Data Transformation Stage"
try:
    print(f">>>>> stage {STAGE_NAME} started <<<<<")
    data_transformation_config =  DataIngestionPipeline()
    data_transformation_config.initiate_data_ingestion()
except Exception as e:
    raise e




STAGE_NAME = "Model Trainer stage"
try:
    print(f">>>>> stage {STAGE_NAME} started <<<<<")
    model_training =  ModelTrainerPipeline()
    model_training.initate_model_training()
except Exception as e:
    raise e
