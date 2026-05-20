import os 
from pathlib import Path 
import logging 

project_name = "student_Performance_p1"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",

    "config/config.yaml",
    "schema.yaml",
    "params.yaml",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/research.ipynb",
    "templates/index.html"
]

for file_path in list_of_files:
    file_path = Path(file_path)

    # Create parent folders if they do not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create the file if it does not exist
    file_path.touch(exist_ok=True)

    logging.info(f"File created: {file_path}")

#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')