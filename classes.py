from abc import ABC, abstractmethod
from enum import Enum
from api import obter_localizacao_cidade, buscar_previsao

class NivelRisco(Enum):
    NENHUM = "NENHUM"
    BAIXO = "BAIXO"
    MEDIO = "MÉDIO"
    ALTO = "ALTO"
    CRITICO = "CRÍTICO"

class LeituraClima:
    def __init__(self, cidade: str, temperatura: float, umidade: float, chuva: float):
        self._validar_dados(temperatura, umidade, chuva)

        self._cidade = cidade
        self._temperatura = temperatura
        self._umidade = umidade
        self._chuva = chuva # Medida em mm

    # * RF1[E]:
    def _validar_dados(self, temperatura: float, umidade: float, chuva: float) -> None:
        if temperatura < -50 or temperatura > 80:
            raise ValueError(f"Temperatura inválida ou ausente")
        if umidade == -999 or not (0 <= umidade <= 100):
            raise ValueError(f"Umidade fora do intervalo [0-100%]: {umidade}%")
        if chuva < 0:
            raise ValueError(f"Taxa de chuva inválida: {chuva} mm/h")

    @property
    def cidade(self) -> str:
        return self._cidade
    
    @property
    def temperatura(self) -> str:
        return self._temperatura

    @property
    def umidade(self) -> str:
        return self._umidade

    @property
    def chuva(self) -> str:
        return self._chuva

    def __repr__(self):
        # Quando faz um print em um objeto da classe, mostra a mensagem 
        # * Ex.: maceio = LeituraClima("Maceió", 22.6, 85, 0)
        # * Ex.: print(maceio) // exibe <Maceió, 22.6°C, 85%, 0mm>
    
        return f"<{self._cidade}, {self._temperatura}°C, {self._umidade}%, {self._chuva}mm>"

# ! Alertas -----------------------

class Alerta(ABC):
    # Classe Abstrata, serve de molde para as outras
    @property
    @abstractmethod
    def nome(self) -> str:
        pass

    @abstractmethod
    def avaliar_risco(self, leitura: LeituraClima) -> NivelRisco:
        pass

    @abstractmethod
    def mensagem_alerta(self, leitura: LeituraClima) -> str:
        pass
        
class AlertaCalor(Alerta):
    @property
    def nome(self) -> str:
        return "Calor extremo"
    
    def avaliar_risco(self, leitura: LeituraClima) -> NivelRisco:
        if leitura.temperatura >= 38 or (leitura.temperatura >= 32 and leitura.umidade >= 80):
            return NivelRisco.ALTO
        elif leitura.temperatura >= 32 or (leitura.temperatura >= 30 and leitura.umidade >= 70):
            return NivelRisco.MEDIO
        elif leitura.temperatura >= 28:
            return NivelRisco.BAIXO
        return NivelRisco.NENHUM
    
    def mensagem_alerta(self, leitura: LeituraClima) -> str:
        return f"⚠️ Alerta de calor: sensação térmica elevada com {leitura.temperatura}°C e umidade de {leitura.umidade}%, mantenha-se hidratado!"
    
class AlertaAlagamento(Alerta):
    @property
    def nome(self) -> str:
        return "Alagamento"

    def avaliar_risco(self, leitura: LeituraClima) -> NivelRisco:
        if leitura.chuva >= 30:
            return NivelRisco.CRITICO
        elif leitura.chuva >= 15:
            return NivelRisco.ALTO
        elif leitura.chuva >= 5:
            return NivelRisco.MEDIO
        elif leitura.chuva > 0:
            return NivelRisco.BAIXO
        return NivelRisco.NENHUM
    
    def mensagem_alerta(self, leitura: LeituraClima):
         return f"🌊 Alerta de alagamento: acúmulo de chuva de {leitura.chuva} mm/h em {leitura.cidade}, evite vias de risco!"

class AlertaGeada(Alerta):    
    @property
    def nome(self) -> str:
        return "Geada"

    def avaliar_risco(self, leitura: LeituraClima) -> NivelRisco:
        if leitura.temperatura <= 0:
            return NivelRisco.ALTO
        elif leitura.temperatura <= 4:
            return NivelRisco.MEDIO
        return NivelRisco.NENHUM
    
    def mensagem_alerta(self, leitura: LeituraClima):
        return f"❄️ Alerta de geada: temperatura crítica de {leitura.temperatura}°C em {leitura.cidade}, proteja hortas e animais!"
    
class AlertaTempestade(Alerta):
    @property
    def nome(self) -> str:
        return "Tempestade"

    def avaliar_risco(self, leitura: LeituraClima) -> NivelRisco:
        if leitura.chuva >= 20 and leitura.umidade >= 85:
            return NivelRisco.ALTO
        elif leitura.chuva >= 10:
            return NivelRisco.MEDIO
        return NivelRisco.NENHUM
    
    def mensagem_alerta(self, leitura: LeituraClima):
        return f"⛈️ Alerta de tempestade: chuva de {leitura.chuva} mm/h com umidade de {leitura.umidade}%, atenção a rajadas de vento e raios!"
 
# ! Provedores --------------------

class ProvedorClima(ABC):
    # Classe Abstrata, serve de molde para as outras
    @abstractmethod
    def obter_leitura(self, cidade) -> LeituraClima:
        pass
    
class ProvedorOpenMeteo(ProvedorClima):
    def obter_leitura(self, cidade: str) -> LeituraClima:
         lat, lon = obter_localizacao_cidade(cidade)
         dados = buscar_previsao(lat, lon)
         
         return LeituraClima(cidade = cidade, temperatura=dados["current"]["temperature_2m"], umidade=dados["current"]["relative_humidity_2m"], chuva=dados["current"]["rain"])

class ProvedorFicticio(ProvedorClima):
    def obter_leitura(self, cidade: str) -> LeituraClima:
        return LeituraClima(
            cidade=cidade,
            temperatura=32.0,
            umidade=45.0,
            chuva=0.0,
        )
        