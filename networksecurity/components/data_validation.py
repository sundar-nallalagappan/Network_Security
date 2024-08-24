import os, sys
import pandas as pd
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.utils.main_utils.utils import read_yaml

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

class DataValidation:
    def __init__(self, 
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH)
            
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def validate_number_of_column(self, dataframe: pd.DataFrame) -> bool:
        try:
            pass
        except Exception as e:
            NetworkSecurityException(e, sys)
    