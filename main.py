

"""
#V1
print("Funcionando 🚀")

from pymongo import MongoClient

client = MongoClient("mongodb+srv://igorinri_db_user:ekA60Dsq20fofetk@cluster0.o0vnn6k.mongodb.net/?appName=Cluster0")
db = client["fitness"]

db = client["fitness"]
db.test.insert_one({"msg": "hello"})

import requests
from pymongo import MongoClient

# CONFIG
STRAVA_TOKEN = "843db69feaedfb23be32a20c3eed0a7ac932e49b" # access_token
#MONGO_URI = "SUA_STRING_MONGO"

# CONEXÃO
client = MongoClient("mongodb+srv://igorinri_db_user:ekA60Dsq20fofetk@cluster0.o0vnn6k.mongodb.net/?appName=Cluster0")
db = client["fitness"]

# API STRAVA
url = "https://www.strava.com/api/v3/athlete/activities"
headers = {"Authorization": f"Bearer {STRAVA_TOKEN}"}

response = requests.get(url, headers=headers)
activities = response.json()

print(f"Atividades encontradas: {len(activities)}")

# 🔥 VALIDAÇÃO
if not isinstance(activities, list):
    print("Erro na API:")
    print(activities)
    exit()

# SALVAR NO MONGO
for act in activities:
    db.activities.update_one(
        {"external_id": act["id"], "source": "strava"},
        {"$set": act},
        upsert=True
    )

print("Importação finalizada 🚀")




#V2
print("🚀 Iniciando pipeline")

import db
#print(dir(db)) #validar dir 

from db import get_db
from strava import fetch_activities
import time

db = get_db()

# 🔹 pegar último processamento
control = db.pipeline_control.find_one({"pipeline": "strava"})
last_run = control["last_run"] if control else 0

print("Último processamento:", last_run)

# 🔹 buscar dados
activities = fetch_activities(after=last_run)

# 🔥 validação
if not isinstance(activities, list):
    print("Erro na API:")
    print(activities)
    exit()

print(f"Atividades encontradas: {len(activities)}")

# 🔹 salvar
for act in activities:
    db.activities.update_one(
        {"external_id": act["id"], "source": "strava"},
        {"$set": act},
        upsert=True
    )

# 🔹 atualizar controle (timestamp atual)
now = int(time.time())

db.pipeline_control.update_one(
    {"pipeline": "strava"},
    {"$set": {"last_run": now}},
    upsert=True
)


now = int(time.time())



latest = max([
    int(datetime.fromisoformat(act["start_date"].replace("Z", "")).timestamp())
    for act in activities
])

db.pipeline_control.update_one(
    {"pipeline": "strava"},
    {"$set": {"last_run": latest}},
    upsert=True
)

print("✅ Importação finalizada")
"""



print("🚀 Iniciando pipeline")

from db import get_db
from strava import fetch_activities
from datetime import datetime

# 🔹 Conecta no Mongo
db = get_db()

# 🔹 Busca controle do pipeline (última execução)
control = db.pipeline_control.find_one({"pipeline": "strava"})
last_run = control["last_run"] if control else 0

print("Último processamento:", last_run)

# 🔹 Busca atividades do Strava usando incremental (after)
activities = fetch_activities(after=last_run)

# 🔥 Validação da resposta da API
if not isinstance(activities, list):
    print("Erro na API:")
    print(activities)
    exit()

print(f"Atividades encontradas: {len(activities)}")

# 🔹 Salva no Mongo (evita duplicidade com upsert)
for act in activities:
    db.activities.update_one(
        {"external_id": act["id"], "source": "strava"},
        {"$set": act},
        upsert=True
    )

# 🔹 Atualiza o controle SOMENTE se vieram dados novos
if activities:
    # Converte start_date (ISO) → timestamp
    latest = max([
        int(datetime.fromisoformat(act["start_date"].replace("Z", "")).timestamp())
        for act in activities
    ])

    db.pipeline_control.update_one(
        {"pipeline": "strava"},
        {"$set": {"last_run": latest}},
        upsert=True
    )

    print("Novo last_run:", latest)
else:
    print("Nenhuma atividade nova, mantendo last_run atual")

print("✅ Importação finalizada")