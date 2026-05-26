from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestConfig:
  root_dir: Path 
  source_URL: str 
  local_data_file: Path 
  unzip_dir: Path 


@dataclass
class DataValidationConfig:
    root_dir: Path
    status_file: str 
    unzipped_data_dir: Path
    all_schema: dict


@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    train_data_path: Path
    test_data_path: Path