import pymongo
from pymongo import MongoClient
#you are a smart bitch,so i think you don't need any commnts
#good luck
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
    def SaveImgSingular(self,imgDict):
        self.__col.insert(imgDict)
        return True
         
    def SaveImgMultiple(self,imgList):
        try:
            return True
            self.__col.insert_many(imgList)
        except Exception as e:
            print e
            return False

