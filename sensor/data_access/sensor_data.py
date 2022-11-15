import sys

import numpy as np
import pandas as pd

from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import COLLECTION_NAME
from sensor.exception import SensorException


class SensorData:
    '''
    This class will help to export data from mongodb as dataframe
    '''
    def __init__(self):
        try:
            self.mongo_client=MongoDBClient()
            
        except Exception as e:
            raise SensorException(e,sys)
    
    def export_collection_as_dataframe(self,collection_name:str=COLLECTION_NAME)->pd.DataFrame:
        try:
            collection=self.mongo_client.database[collection_name]
            df=pd.DataFrame(list(collection.find()))
            
            if '_id' in df.columns:
                df=df.drop(columns=["_id"],axis=1)
                
            df.replace({"na":np.nan},inplace=True)
            
            return df
        
        except Exception as e:
            raise SensorException(e,sys)