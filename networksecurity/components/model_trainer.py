import os
import sys
import numpy as np

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from xgboost import XGBClassifier

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

class ModelTrainer:
    def __init__(self, 
                 model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def perform_hyper_parameter_tuning(self):
        pass
    
    def train_model(self, x, y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x, y)
            return xgb_clf
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_model_trainer(self):
        logging.info("Model trainer started")
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path  = self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array_data(train_file_path)
            test_arr  = load_numpy_array_data(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)
            classification_train_metric = get_classification_score(y_train, y_train_pred)
            
            if classification_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception ("Trained model is not good to provide expected accuracy")
            
            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_test, y_test_pred)
            
            #Overfitting & underfitting
            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)
            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception ("Model is not good for further experimentation")
            
            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            Network_Model = NetworkModel(preprocessor=preprocessor, 
                                         model=model_dir_path)
            save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)
            
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                train_metric_artifact   = classification_train_metric,
                test_metric_artifact    = classification_train_metric
            )
            logging.info("model trainer exited")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
            