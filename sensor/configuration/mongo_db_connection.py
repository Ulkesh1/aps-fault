import pymongo
import os
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
from sensor.exception import SensorException

class MongoDBClient:
    client=None
    def __init__(self,databasename:str=DATABASE_NAME)->None:
        try:
            mongo_url=os.getenv(MONGODB_URL_KEY)
            MongoDBClient.client=pymongo.MongoClient(mongo_url)
            self.client=MongoDBClient.client
            self.database=self.client[databasename]
        except Exception as e:
            raise SensorException(e,sys)