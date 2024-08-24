import os
import sys 
import pandas as pd


'''
defining common constants for training pipeline
'''
TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str  = "Artifacts"
FILE_NAME:str     = "NetworkData.csv"

TRAIN_FILE_NAME:str = "train.csv."
TEST_FILE_NAME:str  = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME  = "model.pkl"
SAVED_MODEL_DIR  = os.path.join("saved_models")
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"


'''
Data Ingestion related constants starts with DATA_INGESTION VAR NAME
'''
DATA_INGESTION_COLLECTION_NAME:str         = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str           = "MLOPS"
DATA_INGESTION_DIR_NAME:str                = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str       = "feature_store"
DATA_INGESTION_INGESTED_DIR:str            = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:str = 0.2


'''
Data validation related constants starts with DATA_VALIDATION VAR NAME
'''
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated" 
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = ""
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = ""
'''
Data Transformation related constants starts with DATA_TRANSFORMATION VAR NAME
'''

'''
Data Trainer related constants starts with DATA_TRAINER VAR NAME
'''