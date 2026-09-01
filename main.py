from classes import ProvedorOpenMeteo, ProvedorFicticio, AlertaAlagamento, AlertaGeada, AlertaCalor, AlertaTempestade, NivelRisco

leitura_api = ProvedorFicticio()
cidade = leitura_api.obter_leitura("Maceió")
print(cidade)

alerta_calor = AlertaCalor()
alerta_alagamento = AlertaAlagamento()
alerta_geada = AlertaGeada()
alerta_tempestade = AlertaTempestade()

# *RF5 [P]:
alertas = [alerta_calor, alerta_alagamento, alerta_geada, alerta_tempestade]

print(f"Relatório para {cidade.cidade}:")
for alerta in alertas:
    risco = alerta.avaliar_risco(cidade)
    
    if risco != NivelRisco.NENHUM:
        print(f"[{risco.value}]:{alerta.mensagem_alerta(cidade)}")