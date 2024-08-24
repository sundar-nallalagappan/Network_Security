import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print('MONGO_DB_URL:', MONGO_DB_URL)

import certifi
print(certifi.where())

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger import logger



class NetWorkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def pushing_data_to_mongo(self, records, database, collection_name):
        try:
            self.database = database
            self.collection_name = collection_name
            self.records = records
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection_name = self.database[self.collection_name]
            self.collection_name.insert_many(self.records)
            return len(self.records)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == '__main__':
    FILE_PATH = "./Network_Data/NetworkData.csv"
    DATABASE  = "MLOPS"
    COLLECTION_NAME = "NetworkData"
    network_data_extract = NetWorkDataExtract()
    records=network_data_extract.csv_to_json(FILE_PATH)
    print(records[0])
    num_rec = network_data_extract.pushing_data_to_mongo(records, DATABASE, COLLECTION_NAME)
    print(f'{num_rec} inserted into mongo DB')