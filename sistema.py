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

    @abstractmethod
    def descrever(self, leitura: LeituraClimatica) -> str:
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

    def descrever(self, leitura: LeituraClimatica) -> str:
        return f"Alerta de calor: sensação térmica elevada com {leitura.temperatura}°C e umidade de {leitura.umidade}%, mantenha-se hidratado!"
    


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

    def descrever(self, leitura: LeituraClimatica) -> str:
        return f"Alerta de alagamento: acúmulo de chuva de {leitura.chuva_mm_h} mm/h em {leitura.cidade}, evite vias de risco!"


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

    def descrever(self, leitura: LeituraClimatica) -> str:
        return f"Alerta de geada: temperatura crítica de {leitura.temperatura}°C em {leitura.cidade}, proteja hortas e animais!"


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

    def descrever(self, leitura: LeituraClimatica) -> str:
        return f"Alerta de tempestade: chuva de {leitura.chuva_mm_h} mm/h com umidade de {leitura.umidade}%, atenção a rajadas de vento e raios!"

leitura_rio = LeituraClimatica("Rio de Janeiro", 39.5, 82.0, 0.0)

leitura_sp = LeituraClimatica("São Paulo", 22.0, 92.0, 35.0)

leitura_gramado = LeituraClimatica("Gramado", -1.5, 70.0, 0.0)

leitura_curitiba = LeituraClimatica("Curitiba", 21.0, 60.0, 0.0)

alerta_calor = AlertaCalor()
alerta_alagamento = AlertaAlagamento()
alerta_geada = AlertaGeada()
alerta_tempestade = AlertaTempestade()

alertas = [alerta_calor, alerta_alagamento, alerta_geada, alerta_tempestade]

leituras = [leitura_rio, leitura_sp, leitura_gramado, leitura_curitiba]

for leitura in leituras:
    print(f"\n=== Relatório para {leitura.cidade} ===")
    print(leitura)  # Chama o __repr__ da classe
    
    for alerta in alertas:
        risco = alerta.avaliar_risco(leitura)
        
        if risco != NivelRisco.NENHUM:
            print(f"[{risco.value}]: {alerta.descrever(leitura)}")
