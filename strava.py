import requests
import os


# 🔹 Token do Strava (depois vamos mover para ENV)
#STRAVA_TOKEN = "8xpto"
STRAVA_TOKEN = os.getenv("STRAVA_TOKEN")

def fetch_activities(after=None):
    """
    Busca atividades do Strava.
    Se 'after' for informado, busca apenas atividades após esse timestamp.
    """

    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {STRAVA_TOKEN}"}

    params = {}
    if after:
        params["after"] = after  # 🔹 incremental

    response = requests.get(url, headers=headers, params=params)

    return response.json()



