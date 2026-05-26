import os 
from src.student_Performance_p1 import logger 
import pandas as pd
from src.student_Performance_p1.config.configuration import DataValidationConfig



class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = None
 
            data = pd.read_csv (self.config.unzipped_data_dir)
            all_cols = list(data.columns)
            
            all_schema= self.config.all_schema.keys() # we get the colon names from the schema file, which is a dictionary, so we use the keys() method to get the column names.
            #all_types = self.config.all_schema.values()
 
            validation_status = all(col in all_schema for col in all_cols)
            with open(self.config.status_file, 'w') as f:
                f.write(f'Validación global: {validation_status}\n')
 
            return validation_status  
        except Exception as e:
            logger.exception(f"Error during column validation: {e}")
            raise e
