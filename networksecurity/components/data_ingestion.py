from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

#configuration & generation of artifactss
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from dotenv import load_dotenv
load_dotenv()
from sklearn.model_selection import train_test_split

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def export_collection_to_dataframe(self):
        print('export_collection_to_dataframe')
        try:
            database_name  =self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            print(f'database_name:', database_name)
            print(f'collection_name:', collection_name)
            print('MONGO_DB_URL:', MONGO_DB_URL)
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            
            
            #print('collection:', list(collection.find()))
            df = pd.DataFrame(list(collection.find()))
            #print('df:', df)
            print("Records from DB",df.shape)
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            
            df.replace({'na':np.nan}, inplace=True)
            
            return df
            
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def export_data_to_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
            
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def split_date_as_train_test(self, dataframe: pd.DataFrame):
        print('split_date_as_train_test')
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            print(train_set.shape, test_set.shape)
            logging.info("Exporting train-test file to directories")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            print('dir_path:', dir_path)
            os.makedirs(dir_path, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            
            dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path, exist_ok=True)
            print('dir_path:',dir_path)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Train-test file export success")
            
        except Exception as e:
            NetworkSecurityException(e, sys)
            
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_to_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_date_as_train_test(dataframe=dataframe)
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                  test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
            
        except Exception as e:
            NetworkSecurityException(e, sys )
        
        