import pymongo
from pymongo import MongoClient
class Mongo:
    
    def __init__(self,ip,port,database,collection):
        self.__ip = ip
        self.__port = port
        self.__database = database
        self.__collection = collection
    def _connectMongo(self):
        self.__client = MongoClient(self.__ip,self.__port)
        self.__db = self.__client[self.__database]
        self.__col = self.__db[self.__collection]
        
    def OpenConn(self):
        try:
            self._connectMongo()
            return True
        except Exception as e:
            print e
            return False
    def SaveURLInfo(self,imgDict):
        self.__col.insert(imgDict)
        return True
         

