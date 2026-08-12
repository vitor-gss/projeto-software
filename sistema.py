from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple

class NivelRisco(Enum):
    NENHUM = "NENHUM"
    BAIXO = "BAIXO"
    MEDIO = "MÉDIO"
    ALTO = "ALTO"
    CRITICO = "CRÍTICO"


class LeituraClimatica:
    def __init__(self, cidade: str, temperatura: float, umidade: float, chuva_mm_h: float):
        self._validar_dados(temperatura, umidade, chuva_mm_h)
        
        self._cidade = cidade
        self._temperatura = float(temperatura)
        self._umidade = float(umidade)
        self._chuva_mm_h = float(chuva_mm_h)

    def _validar_dados(self, temp: float, umidade: float, chuva: float) -> None:
        if temp is None or umidade is None or chuva is None:
            raise ValueError("Dado ausente na resposta da API (None)")
        else:
            if temp == -999 or temp < -100 or temp > 70:
                raise ValueError(f"Temperatura inválida ou ausente: {temp}°C")
            
            if umidade == -999 or not (0 <= umidade <= 100):
                raise ValueError(f"Umidade fora do intervalo [0-100%]: {umidade}%")
            
            if chuva == -999 or chuva < 0:
                raise ValueError(f"Taxa de chuva inválida: {chuva} mm/h")

    @property
    def cidade(self) -> str:
        return self._cidade

    @property
    def temperatura(self) -> float:
        return self._temperatura

    @property
    def umidade(self) -> float:
        return self._umidade

    @property
    def chuva_mm_h(self) -> float:
        return self._chuva_mm_h

    def __repr__(self) -> str:
        return f"<LeituraClimatica {self._cidade}: {self._temperatura}°C, {self._umidade}%, {self._chuva_mm_h}mm/h>"

class CategoriaAlerta(ABC):
    @property
    @abstractmethod
    def nome(self) -> str:
        pass

    @abstractmethod
    def avaliar_risco(self, leitura: LeituraClimatica) -> NivelRisco:
        pass


class AlertaCalor(CategoriaAlerta):    
    @property
    def nome(self) -> str:
        return "Calor Extremo"

    def avaliar_risco(self, leitura: LeituraClimatica) -> NivelRisco:
        if leitura.temperatura >= 38 or (leitura.temperatura >= 32 and leitura.umidade >= 80):
            return NivelRisco.ALTO
        elif leitura.temperatura >= 32 or (leitura.temperatura >= 30 and leitura.umidade >= 70):
            return NivelRisco.MEDIO
        elif leitura.temperatura >= 28:
            return NivelRisco.BAIXO
        return NivelRisco.NENHUM


class AlertaAlagamento(CategoriaAlerta):
    @property
    def nome(self) -> str:
        return "Alagamento"

    def avaliar_risco(self, leitura: LeituraClimatica) -> NivelRisco:
        if leitura.chuva_mm_h >= 30:
            return NivelRisco.CRITICO
        elif leitura.chuva_mm_h >= 15:
            return NivelRisco.ALTO
        elif leitura.chuva_mm_h >= 5:
            return NivelRisco.MEDIO
        elif leitura.chuva_mm_h > 0:
            return NivelRisco.BAIXO
        return NivelRisco.NENHUM


class AlertaGeada(CategoriaAlerta):    
    @property
    def nome(self) -> str:
        return "Geada"

    def avaliar_risco(self, leitura: LeituraClimatica) -> NivelRisco:
        if leitura.temperatura <= 0:
            return NivelRisco.ALTO
        elif leitura.temperatura <= 4:
            return NivelRisco.MEDIO
        return NivelRisco.NENHUM


class AlertaTempestade(CategoriaAlerta):
    @property
    def nome(self) -> str:
        return "Tempestade"

    def avaliar_risco(self, leitura: LeituraClimatica) -> NivelRisco:
        if leitura.chuva_mm_h >= 20 and leitura.umidade >= 85:
            return NivelRisco.ALTO
        elif leitura.chuva_mm_h >= 10:
            return NivelRisco.MEDIO
        return NivelRisco.NENHUM
