import os, sys
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

class DataValidation:
    def __init__(self, 
                 data_validation_config: DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config  = data_validation_config
            self._schema_config          = read_yaml_file(SCHEMA_FILE_PATH)
            #print('self._schema_config:', self._schema_config)
            
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def validate_number_of_column(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_cols=len(self._schema_config["columns"])
            logging.info(f'Number of required columns {number_of_cols}')
            logging.info(f'Number of columns in df {len(dataframe.columns)}')
            
            if number_of_cols == len(dataframe.columns):
                return True
            else:
                return False
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns  = self._schema_config['numerical_columns']
            dataframe_columns  = dataframe.columns
            
            numerical_column_present  = True
            missing_numerical_columns = []
            
            for col in numerical_columns:
                if col not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(col)
                    
            logging.info(f"Missing numeircal columns: {missing_numerical_columns}")
            return numerical_column_present
            
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        print('detect_dataset_drift')
        try:
            status = True
            report = {}
            
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "P-value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            
            print('report:', report)
                    
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            print('drift_report_file_path:', drift_report_file_path)
            
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            
            write_yaml_file(file_path=drift_report_file_path, 
                            content=report)
            
            return status
            
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path  = self.data_ingestion_artifact.test_file_path
            
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe  = DataValidation.read_data(test_file_path)
            
            status_train = self.validate_number_of_column(dataframe=train_dataframe)
            if not status_train:
                error_message=f"{error_message} Train dataframe does not contain all columns \n"
            status_test = self.validate_number_of_column(dataframe=test_dataframe)
            if not status_test:
                error_message=f"{error_message} Test dataframe does not contain all columns \n"                
                
            status_drift = self.detect_dataset_drift(base_df=train_dataframe,
                                               current_df=test_dataframe)
            
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_validation_config.invalid_train_file_path), exist_ok=True)
            if status_train and status_drift:
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            else:
                train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
                
            if status_test and status_drift:                
                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            else:
                test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)
            
            data_validation_artifact = DataValidationArtifact(
                    validation_status       = status_drift,
                    valid_train_file_path   = self.data_validation_config.valid_train_file_path,
                    valid_test_file_path    = self.data_validation_config.valid_test_file_path,
                    invalid_train_file_path = None,
                    invalid_test_file_path  = None,
                    drift_report_file_path  = self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    