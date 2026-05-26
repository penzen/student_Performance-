import requests
import tarfile
from src.student_Performance_p1.entity.config_entity import DataIngestConfig


class DataIngestor:
    def __init__(self, config: DataIngestConfig):
        # Store the data ingestion configuration
        # This config contains:
        # - source_URL
        # - local_data_file
        # - unzip_dir
        self.config = config

    def download_data(self):
        # Download the dataset from the source URL
        response = requests.get(self.config.source_URL)

        # If the URL is wrong or download fails, this will raise an error
        response.raise_for_status()

        # Save the downloaded file locally
        # Example: artifacts/data_ingestion/housing.tgz
        with open(self.config.local_data_file, "wb") as f:
            f.write(response.content)

        print(f"Data downloaded successfully to: {self.config.local_data_file}")

    def unzip_data(self):
        # Your dataset is a .tgz file, not a .zip file
        # So we use tarfile instead of zipfile
        with tarfile.open(self.config.local_data_file, "r:gz") as tar_ref:
            tar_ref.extractall(path=self.config.unzip_dir)

        print(f"Data extracted successfully to: {self.config.unzip_dir}")