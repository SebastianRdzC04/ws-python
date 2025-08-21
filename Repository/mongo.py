from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://admin:admin123@atenasoficial.com:5000/autsorce?authSource=admin"
 
   # Cree una conexión con MongoClient. Puede importar MongoClient o usar pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Cree la base de datos para nuestro ejemplo (usaremos la misma base de datos en todo el tutorial
   return client['db_cathub']


class Mongo:

    @staticmethod
    def get_collection(collection_name: str):
        dbname = get_database()
        return dbname[collection_name]
    

    @staticmethod
    def check_connection():
        try:
            client = MongoClient("mongodb://admin:admin123@atenasoficial.com:5000/autsorce?authSource=admin", serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
        except Exception as e:
            print("Error al conectar a MongoDB")
            return False
        return True
