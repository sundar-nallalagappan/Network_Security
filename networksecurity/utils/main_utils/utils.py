import yaml
import pickle
import dill 
import os, sys
import numpy as np 

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
        

def write_yaml_file(file_path:str, content: object, replace: bool = False) -> None:
    print('write-yaml-file:', file_path)
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            yaml.dump(content, yaml_file)
            print("drift report success")
    except Exception as e:
        print(e)
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
def load_numpy_array_data(file_path:str) -> np.array:
    '''
    load numpy array data from the file
    file_path: str - location of the numpy file
    return np.array data
    '''
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_object(file_path:str, obj: object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object methods of Mainutils utils")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_object(file_path:str) -> object:
    
    if not os.path.exists(file_path):
        raise Exception(f"The file path {file_path} does not exists")
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
            
        
        
        


