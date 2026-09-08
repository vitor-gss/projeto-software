from abc import ABC, abstractmethod
import requests
from sistema import LeituraClimatica

class ProvedorClimatico(ABC):
    @abstractmethod
    def obter_leitura(self, cidade: str, lat: float, lon: float) -> LeituraClimatica:
        pass

class ProvedorFalso(ProvedorClimatico):
    DADOS = {
        "Maceió":   (34, 85, 10),    # o exemplo do enunciado
        "Recife":   (30, 70, 35),    # alagamento CRÍTICO
        "Curitiba": (-1, 60, 0),     # geada ALTO
    }

    def obter_leitura(self, cidade, lat, lon):
        if cidade not in self.DADOS: #Messias - Adicionei essa linha
            raise ValueError(f"Cidade '{cidade}' não encontrada nos dados") #Messias - Adicionei essa linha
        temp, umid, chuva = self.DADOS[cidade]
        return LeituraClimatica(cidade, temp, umid, chuva)

##############################################################################################################################################
class OpenMeteoProvider(ProvedorClimatico):
    URL = "https://api.open-meteo.com/v1/forecast"
    # Cache compartilhado entre todas as instâncias, caso se desejar
    _session = None
    
    @classmethod
    def _get_session(cls):
        if cls._session is None:
            # expire_after=300 segundos = 5 minutos
            cls._session = requests_cache.CachedSession(
                'clima_cache', 
                expire_after=300,
                allowable_methods=('GET',),  # Apenas GET requests
            )
        return cls._session

    def __init__(self, use_cache=True):
        """
        Args:
            use_cache: Se False, ignora o cache (útil para testes)
        """
        self.use_cache = use_cache
        if use_cache:
            self.session = self._get_session()
        else:
            self.session = requests.Session()  # Fallback para testes

    def obter_leitura(self, cidade: str, lat: float, lon: float) -> LeituraClimatica:
        # Avisa se está usando cache (útil para debugging)
        if self.use_cache:
            cache_key = f"{lat}_{lon}"  # requests_cache faz isso internamente
            # Não precisamos verificar manualmente - a biblioteca faz isso!
        
        resposta = self.session.get(
            self.URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation",
            },
            timeout=10,  # Adiciona timeout para evitar travamentos
        )
        resposta.raise_for_status()
        
        # Verifica se veio do cache (opcional, para debugging)
        if hasattr(resposta, 'from_cache') and resposta.from_cache:
            print(f"  [CACHE] Dados de {cidade} carregados do cache")
        else:
            print(f"  [REDE] Dados de {cidade} carregados da API")
        
        atual = resposta.json()["current"]
        
        return LeituraClimatica(
            cidade = cidade,
            temperatura = atual["temperature_2m"],
            umidade = atual["relative_humidity_2m"],
            chuva_mm_h = atual["precipitation"],
        )




###############################################################################################################################################

# VERSÃO ANTIGA
"""
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

"""
