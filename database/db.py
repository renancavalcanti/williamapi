from pymongo import MongoClient

class Database():
    def __init__(self, database_name = None, connectrion_string = None):
        if database_name==None or connectrion_string==None:
            raise Exception("MongoBD requires database name and string connection!")
        
        self.__database_name = database_name
        self.__connectrion_string = connectrion_string
        self.__db_connection = None
        self.__database = None
    
    @property
    def database(self):
        return self.__database
        
    def connect(self):
        try:
            self.__db_connection = MongoClient(self.__connectrion_string)
            db_name = str(self.__database_name)
            self.__database = self.__db_connection[db_name]
        except:
            print("Mongo connection error!")
    