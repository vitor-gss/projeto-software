from abc import ABC, abstractmethod
import requests
from sistema import LeituraClimatica

class ProvedorClimatico(ABC):
    @abstractmethod
    def pegar_leitura(self, cidade: str, lat: float, lon: float) -> LeituraClimatica:
        pass

class OpenMeteoProvider(ProvedorClimatico):
    URL = "https://api.open-meteo.com/v1/forecast"

    def obter_leitura(self, cidade: str, lat: float, lon: float) -> LeituraClimatica:
        resposta = requests.get(
            self.URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation",
            },
        )
        resposta.raise_for_status()
        atual = resposta.json()["current"]

        return LeituraClimatica(
            cidade = cidade,
            temperatura = atual["temperature_2m"],
            umidade = atual["relative_humidity_2m"],
            chuva_mm_h = atual["precipitation"],
        )