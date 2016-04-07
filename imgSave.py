import pymongo
from pymongo import MongoClient

class Mongo:
    #.ctor
    def __init__(self,ip,port,database,collection):
        self.__ip = ip
        self.__port = port
        self.__database = database
        self.__collection = collection
    def _connectMongo(self):
        self.__client = MongoClient(self.__ip,self.__port)
        self.__db = self.__client[self.__database]
        self.__col = self.__db[self.__collection]
    #open connection, return true while success
    def OpenConn(self):
        try:
            self._connectMongo()
            return True
        except Exception as e:
            print e
            return False
    #function which allow to save a image , which will take a dict argument
    def SaveImgSingular(self,imgDict):
        self.__col.insert(imgDict)
        return True
    #function which allow to save images , which will take a dict argument which contains all the infomation.     
    def SaveImgMultiple(self,imgList):
        try:
            return True
            self.__col.insert_many(imgList)
        except Exception as e:
            print e
            return False

