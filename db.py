from pymongo import MongoClient

def get_db():
    """
    Cria conexão com MongoDB e retorna o database 'fitness'
    """
    client = MongoClient("mongodb+srv://igorinri_db_user:ekA60Dsq20fofetk@cluster0.o0vnn6k.mongodb.net/?appName=Cluster0")
    return client["fitness"]