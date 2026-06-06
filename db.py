import os
from pymongo import MongoClient

def get_db():
    """
    Cria conexão com MongoDB e retorna o database 'fitness'
    """
    print("MONGO_URI:", os.getenv("MONGO_URI"))

    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise Exception("MONGO_URI não definida")


    #client = MongoClient("mongodb+srv://igorinri_db_user:ekA60Dsq20fofetk@cluster0.o0vnn6k.mongodb.net/?appName=Cluster0")
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["fitness"]
