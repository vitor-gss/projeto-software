import requests 
from classes import (ResultadoCidade, ProvedorOpenMeteo, ProvedorFicticio, AlertaAlagamento, AlertaGeada, AlertaCalor, AlertaTempestade, NivelRisco)
from cidades import cidades

# * RF6 [A/IF] — Provedores de dados intercambiáveis. 
leitura_api = ProvedorOpenMeteo()
# leitura_api = ProvedorFicticio()

alerta_calor = AlertaCalor()
alerta_alagamento = AlertaAlagamento()
alerta_geada = AlertaGeada()
alerta_tempestade = AlertaTempestade()

alertas = [alerta_calor, alerta_alagamento, alerta_geada, alerta_tempestade]

def leitura_unica_cidade(provedor, cidade):
    try:
        leitura = provedor.obter_leitura(cidade)
    except ValueError as e:
        print(f" [dado invalido] {e}")
        return 
    # Para quando estiver sem internet
    except requests.RequestException as e: 
        print(f" [falha de rede] {e}")
        return
    
    imprimir_relatorio(leitura)

# Analisa quais nao tem risco nenhum para nao imprimir ()
def avaliar_alertas_ativos(leitura):
    alertas_ativos = []
    for alerta in alertas: # * RF5 [P] — Avaliação uniforme.
        nivel = alerta.avaliar_risco()
        if nivel != NivelRisco.NENHUM:
            alertas_ativos.append((alerta.mensagem_alerta(leitura), nivel))
        return alertas_ativos

def coletar_resultados(provedor):
    resultados = []
    for cidade in cidades:
        try:
            leitura = provedor.obter_leitura(cidade)
        except ValueError as e:
            resultados.append(ResultadoCidade(cidade, None, [], str(e)))
            continue
        except requests.RequestException as e:
            resultados.append(ResultadoCidade(cidade, None, [], f"falha de rede: {e}"))
            continue
        alertas_ativos = avaliar_alertas_ativos(leitura)
        resultados.append(ResultadoCidade(cidade, leitura, alertas_ativos, ""))
    return resultados
        
def imprimir_detalhado(resultados):
    for res in resultados:
        print(f"\n{res.cidade} :")
        if res.erro:
            print(f" [dado inválido] {res.erro}")
            continue
        print(f"  {res.leitura.temperatura}°C ; {res.leitura.umidade}% ; {res.leitura.chuva}mm/h")
        for nome, nivel in res.alertas_ativos:
            print(f"{nome | {nivel.value}}")
            
def imprimir_relatorio(leitura):
    print(f"{leitura.temperatura}°C ; {leitura.umidade}% ; {leitura.chuva}mm/h.")
    for alerta in alertas:
        nivel = alerta.avaliar_risco(leitura)
        print(f"{alerta.mensagem_alerta(leitura)} | {nivel.value}")

# try:
#     leitura = leitura_api.obter_leitura("São Paulo")
# except ValueError as e:
#     print(f"[erro] {e}")
# except requests.RequestException as e:
#     print(f"[falha de rede] {e}")
# else:
#     print(leitura)
#     print(f"Relatório para {leitura.cidade}:")
#     for alerta in alertas:
#         risco = alerta.avaliar_risco(leitura)
#         if risco != NivelRisco.NENHUM:
#             print(f"[{risco.value}]: {alerta.mensagem_alerta(leitura)}")
            
def main():

    while True:
        print("1 - Relatório de uma cidade")
        print("2 - Relatório de todas as cidades")
        print("3 - Relatório consolidado")
        print("4 - SAIR")
        escolha = input("Digite o número da opção que deseja\n")

        if escolha == "1":
            # for cidade in cidades:
            #     print(f"-> {cidade}")
            cidade_digitada = input("Digite o nome da cidade que deseja\n")

            leitura_unica_cidade(leitura_api, cidade_digitada)
        elif escolha == "2":
            resultados = coletar_resultados(leitura_api)
            imprimir_detalhado(resultados)
        # elif escolha == "3":
        #     resultados = coletar_resultados(provedor)
        #     exportar_csv(resultados)
            # print("\nResultado entregue!\n\n")
        elif escolha == "4":
            break
        else:
            print("Escolha um número existente.")
            
main()