import openmeteo_requests
import requests

import pandas as pd
import requests_cache
from retry_requests import retry

def obter_localizacao_cidade(cidade: str) -> tuple[float, float]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": cidade,
        "count": 1,
        "language": "pt",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()

    resultado = data["results"][0]
    return resultado["latitude"], resultado["longitude"]

# ! ------------

def buscar_previsao(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,rain",
    }
    response = requests.get(url, params=params)
    return response.json()
