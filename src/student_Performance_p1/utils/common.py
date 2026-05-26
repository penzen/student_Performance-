import os 
from pathlib import Path
import yaml 
import json 
from src.student_Performance_p1 import logger
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (str): The file path to the YAML file.
    
    Raises:
        ValueError: If there is an error while reading the YAML file or converting its content to ConfigBox.

    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox object.
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file '{path_to_yaml}' Loading successfully.")
            return ConfigBox(content)
    except BoxValueError as e:
        logger.error(f"Error while converting YAML content to ConfigBox: {e}")
        raise ValueError(f"Error while converting YAML content to ConfigBox: {e}")
    except Exception as e:
        logger.error(f"Error while reading YAML file: {e}")
        raise ValueError(f"Error while reading YAML file: {e}")
        


#@ensure_annotations
def create_directories(path_to_directories: list) -> None:
    """
    Creates directories if they do not exist.

    Args:
        path_to_directories (list): A list of directory paths to be created.
    
    Raises:
        ValueError: If there is an error while creating the directories.
    """

    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
        logger.info(f"Directories created successfully: {path_to_directories}")
    except Exception as e:
        logger.error(f"Error while creating directories: {e}")
        raise ValueError(f"Error while creating directories: {e}")





@ensure_annotations
def save_json(path: str, data: Any) -> None:
    """
    Saves data to a JSON file.

    Args:
        path (str): The file path where the JSON file will be saved.
        data (Any): The data to be saved in the JSON file.
    
    Raises:
        ValueError: If there is an error while saving the data to a JSON file.
    """

    try:
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=4)
            logger.info(f"Data successfully saved to JSON file at '{path}'.")
    except Exception as e:
        logger.error(f"Error while saving data to JSON file: {e}")
        raise ValueError(f"Error while saving data to JSON file: {e}")
    
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads data from a JSON file.

    Args:
        path (str): The file path to the JSON file.

    Raises:
        ValueError: If there is an error while loading the data from the JSON file.

    Returns:
        ConfigBox: The data loaded from the JSON file.
    """
    try:
        with open(path) as json_file:
            data = json.load(json_file)
            logger.info(f"Data successfully loaded from JSON file at '{path}'.")
            return ConfigBox(data)
    except Exception as e:
        logger.error(f"Error while loading data from JSON file: {e}")
        raise ValueError(f"Error while loading data from JSON file: {e}")
    


def save_bin(data: Any, path: Path) -> None:
    """
    Saves data to a binary file using joblib.

    Args:
        data (Any): The data to be saved.
        path (str): The file path where the binary file will be saved.
    
    Raises:
        ValueError: If there is an error while saving the data to a binary file.
    """

    try:
        joblib.dump(data, path)
        logger.info(f"Data successfully saved to binary file at '{path}'.")
    except Exception as e:
        logger.error(f"Error while saving data to binary file: {e}")
        raise ValueError(f"Error while saving data to binary file: {e}")
    

def load_bin(path: Path) -> Any:
    """
    Loads data from a binary file using joblib.

    Args:
        path (str): The file path to the binary file.

    Raises:
        ValueError: If there is an error while loading the data from the binary file.

    Returns:
        Any: The data loaded from the binary file.
    """
    try:
        data = joblib.load(path)
        logger.info(f"Data successfully loaded from binary file at '{path}'.")
        return data
    except Exception as e:
        logger.error(f"Error while loading data from binary file: {e}")
        raise ValueError(f"Error while loading data from binary file: {e}")