import sys
import os
import numpy as np 
import pandas as pd 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (
    DataValidationArtifact,
    DataTransformationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging


class DataTransformation:
    def __init__(self,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact     = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_transformer_object(cls) -> Pipeline:
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f'KNNImputer initialized with params {DATA_TRANSFORMATION_IMPUTER_PARAMS}')
            
            preprocessor: Pipeline = Pipeline([("imputer", imputer)])
            
            logging.info("Exiting the preprocessor method of data_transformation class")
            
            return preprocessor
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiating the data transformation")
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df  = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            preprocessor = self.get_transformer_object()
            
            #Train DF
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            
            #Test DF
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            traansformed_input_feature_train_df = preprocessor_object.transform(input_feature_train_df)
            traansformed_input_feature_test_df  = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[traansformed_input_feature_train_df, np.array(target_feature_train_df)]
            test_arr  = np.c_[traansformed_input_feature_test_df, np.array(target_feature_test_df)]
            
            print('train_arr:', train_arr)
            print('test_arr:', test_arr)
            
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, 
                                  array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, 
                                  array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,
                        obj=preprocessor_object)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path  = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path   = self.data_transformation_config.transformed_test_file_path
            )
            logging.info("Data transformation complated")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
            