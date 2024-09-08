import os
import sys 
import pandas as pd
import numpy as np

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
DATA_VALIDATION_DIR_NAME: str               = "data_validation"
DATA_VALIDATION_VALID_DIR: str              = "validated" 
DATA_VALIDATION_INVALID_DIR: str            = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str       = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
'''
Data Transformation related constants starts with DATA_TRANSFORMATION VAR NAME
'''
DATA_TRANSFORMATION_DIR_NAME: str               = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str    = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values": np.nan,
    "n_neighbors"   : 3,
    "weights"       : "uniform"
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str  = "test.npy"

'''
Model Trainer related constants starts with DATA_TRAINER VAR NAME
'''
MODEL_TRAINER_DIR_NAME: str                               = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str                      = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str                     = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float                       = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05


'''
Model Evaluation related constants starts with DATA_TRAINER VAR NAME
'''
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = "0.02"
MODEL_EVALUATION_REPORT_NAME: str = "report.yaml"

'''
Model pusher related constants starts with DATA_TRAINER VAR NAME
'''
MODEL_PUSHER_DIR_NAME:str = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR: str = SAVED_MODEL_DIR



