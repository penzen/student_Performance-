from src.student_Performance_p1.constants import * 
from src.student_Performance_p1.utils.common import read_yaml, create_directories
from src.student_Performance_p1.entity.config_entity import DataIngestConfig, DataTransformationConfig, DataValidationConfig

class ConfigurationManager:
    def __init__(self):
        # Read config.yaml
        self.config = read_yaml(CONFIG_FILE_PATH)

        # Read params.yaml
        self.params = read_yaml(PARAMS_FILE_PATH)

        # Read schema.yaml
        self.schema = read_yaml(SCHEMA_FILE_PATH)

        # Create main artifacts folder
        create_directories([self.config.artifacts_root])

    def get_data_ingest_config(self) -> DataIngestConfig:
        # Access data_ingestion section from config.yaml
        config = self.config.data_ingestion

        # Create data ingestion folder
        create_directories([config.root_dir])

        # Create DataIngestConfig object
        data_ingest_config = DataIngestConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingest_config
    


def get_data_validation_config(self) -> DataValidationConfig:
        # Access data_validation section from config.yaml
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        # Create data validation folder
        create_directories([config.root_dir])

        # Create DataValidationConfig object
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            status_file=config.status_file,
            unzipped_data_dir=config.unzipped_data_dir,
            all_schema=self.schema.COLUMNS
        )

        return data_validation_config



def get_data_transformation_config(self) -> DataTransformationConfig:
        # Access data_transformation section from config.yaml
        config = self.config.data_transformation

        # Create data transformation folder
        create_directories([config.root_dir])

        # Create data transformation config object
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            train_data_path=config.transformed_train_data,
            test_data_path=config.transformed_test_data
        )

        return data_transformation_config
    