import requests

# 🔹 Token do Strava (depois vamos mover para ENV)
STRAVA_TOKEN = "843db69feaedfb23be32a20c3eed0a7ac932e49b"

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



