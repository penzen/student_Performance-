from student_Performance_p1.src.student_Performance_p1.components.data_ingestion import DataIngestor
from student_Performance_p1.src.student_Performance_p1.config.configuration import ConfigurationManager


STAGE_NAME = "Data Ingestion Stage"


class DataIngestionPipeline:
    def __init__(self):
        pass
        #self.config = ConfigurationManager()

    def initiate_data_ingestion(self):
        config_manager = ConfigurationManager()

        data_ingest_config = config_manager.get_data_ingest_config()
        data_ingestion = DataIngestor(config=data_ingest_config)
        data_ingestion.download_data()
        data_ingestion.unzip_data()



if __name__ == "__main__":
    try:
        print(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataIngestionPipeline()
        obj.initiate_data_ingestion()
        print(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
    except Exception as e:
        print(e)
        raise e