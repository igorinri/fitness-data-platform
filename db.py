Cluster0 os
from pymongo import MongoClient

def get_db():
    """
    Cria conexão com MongoDB e retorna o database 'fitness'
    """
    print("MONGO_URI:", os.getenv("MONGO_URI"))

    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise Exception("MONGO_URI não definida")

    client = MongoClient(os.getenv("MONGO_URI"))
    return client["fitness"]
