import os
import sys
import shutil
import pandas as pd

from networksecurity.entity.config_entity import ModelPusherConfig
from networksecurity.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

class ModelPusher:
    def __init__(self,
                 model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_model_pusher(self):
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            
            model_file_path = self.model_pusher_config.model_file_path
            dir_path = os.path.dirname(model_file_path)
            os.makedirs(dir_path, exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)
            
            #saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)
            
            model_pusher_artifact = ModelPusherArtifact(
                    saved_model_path =  saved_model_path,
                    model_file_path  =  trained_model_path
            )
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)