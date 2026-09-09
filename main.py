import requests

from classes import (ProvedorOpenMeteo, ProvedorFicticio, AlertaAlagamento,
                     AlertaGeada, AlertaCalor, AlertaTempestade, NivelRisco)

leitura_api = ProvedorFicticio()

alerta_calor = AlertaCalor()
alerta_alagamento = AlertaAlagamento()
alerta_geada = AlertaGeada()
alerta_tempestade = AlertaTempestade()

# RF5
alertas = [alerta_calor, alerta_alagamento, alerta_geada, alerta_tempestade]

try:
    leitura = leitura_api.obter_leitura("Maceió")
except ValueError as e:
    print(f"[erro] {e}")
except requests.RequestException as e:
    print(f"[falha de rede] {e}")
else:
    print(leitura)
    print(f"Relatório para {leitura.cidade}:")
    for alerta in alertas:
        risco = alerta.avaliar_risco(leitura)
        if risco != NivelRisco.NENHUM:
            print(f"[{risco.value}]: {alerta.mensagem_alerta(leitura)}")