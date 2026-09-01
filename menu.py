import requests
import csv
import unicodedata

from sistema import (AlertaTempestade, AlertaGeada, AlertaCalor, AlertaAlagamento)
from sistema import NivelRisco, LeituraClimatica
from provedor import OpenMeteoProvider, ProvedorFalso

# RF7 multiplas localidades
cidades = [
    ("Maceió",   -9.6658, -35.7353),
    ("Recife",   -8.0476, -34.8770),
    ("Curitiba", -25.4284, -49.2733),
]

alertas = [AlertaAlagamento(), AlertaTempestade(), AlertaGeada(), AlertaCalor()]

class ResultadoCidade:
    def __init__(self, cidade: str, leitura: LeituraClimatica, ativos: list, erro: str):
        self._cidade = cidade
        self._leitura = leitura
        self._ativos = list(ativos)
        self._erro = erro

    @property
    def cidade(self) -> str:
        return self._cidade

    @property
    def leitura(self) -> LeituraClimatica:
        return self._leitura
    
    @property
    def ativos(self) -> list:
        return self._ativos

    @property
    def erro(self) -> str:
        return self._erro


def avaliar_ativos(leitura): #Analisa quais nao tem risco nenhum para nao imprimir ()
    ativos = []
    for alerta in alertas: # RF5: laço genérico, não sabe qual categoria processa
        nivel = alerta.avaliar_risco(leitura)
        if nivel != NivelRisco.NENHUM:
            ativos.append((alerta.descrever(leitura), nivel)) # RF4
    return ativos

def coletar_resultados(provedor): #mostra todas as cidades
    resultados = []
    for cidade,lat,lon in cidades:
        try:
            leitura = provedor.obter_leitura(cidade, lat, lon)
        except ValueError as e:
            resultados.append(ResultadoCidade(cidade, None, [], str(e)))
            continue
        except requests.RequestException as e:
            resultados.append(ResultadoCidade(cidade, None, [], f"falha de rede: {e}"))
            continue
        ativos = avaliar_ativos(leitura)
        resultados.append(ResultadoCidade(cidade, leitura, ativos, ""))
    return resultados

def imprimir_detalhado(resultados):
    for r in resultados:
        print(f"\n{r.cidade} :")
        if r.erro:
            print(f"  [dado inválido] {r.erro}")
            continue
        print(f"  {r.leitura.temperatura}°C ; {r.leitura.umidade}% ; {r.leitura.chuva_mm_h}mm/h")
        for nome, nivel in r.ativos:
            print(f"  {nome} | {nivel.value}")

def imprimir_relatorio(leitura):
    print(f"{leitura.temperatura}°C ; {leitura.umidade}% ; {leitura.chuva_mm_h}mm/h.")
    for alerta in alertas:
        nivel = alerta.avaliar_risco(leitura)
        print(f"{alerta.descrever(leitura)} | {nivel.value}") # RF4

def leitura_unica(provedor, escolha_cidade): #leitura da cidade
    lat, lon = None, None

    for cidade, latitude, longitude in cidades:
        if cidade == escolha_cidade:
            lat = latitude
            lon = longitude

    if lat is None or lon is None:
        print("Cidade não cadastrada.")
        return

    try:
        leitura = provedor.obter_leitura(escolha_cidade, lat, lon)
    except ValueError as e:
        print(f" [dado invalido] {e}")
        return 
    except requests.RequestException as e: #para quando estiver sem internet
        print(f" [falha de rede] {e}")
        return

    imprimir_relatorio(leitura)

def exportar_csv(resultados, arquivo="relatorio.csv"):
    with open(arquivo, "w", newline="", encoding="utf-8-sig") as file:
        escritor = csv.writer(file, delimiter=";")
        escritor.writerow(["Cidade", "Temperatura (°C)", "Umidade (%)", 
                              "Chuva (mm/h)", "Alertas ativos"])

        for r in resultados:
            if r.erro:
                escritor.writerow([r.cidade, "", "", "", f"ERRO: {r.erro}"])
            else:
                if r.ativos:
                    partes = []
                    for descricao, nivel in r.ativos: #puxa a desc e o nivel 
                        partes.append(f"{descricao} {nivel.value}") #dos ativos da funcao avaliar_ativos 
                    texto = " | ".join(partes)
                else:
                    texto = "S/ alertas"

                escritor.writerow([r.cidade, r.leitura.temperatura, r.leitura.umidade,
                    r.leitura.chuva_mm_h, texto])
                

def menu():

    provedor = ProvedorFalso() # RF6 Falso por enquanto, só trocar depois
    #ja testei com o OpenMeteoProvider() e deu certo. apenas trocar o print das cidades na opção 1
    while True:

        print("1 - Relatório de uma cidade")
        print("2 - Relatório de todas as cidades")
        print("3 - Relatório consolidado")
        print("4 - SAIR")
        escolha = input("Digite o número da opção que deseja\n")

        if escolha == "1":
            for cidade, _, _ in cidades:
                print(f"-> {cidade}");
            escolha_cidade = input("Digite o nome da cidade que deseja\n")
            leitura_unica(provedor, escolha_cidade)
        elif escolha == "2":
            resultados = coletar_resultados(provedor)
            imprimir_detalhado(resultados)
        elif escolha == "3":
            resultados = coletar_resultados(provedor)
            exportar_csv(resultados)
            print("\nResultado entregue!\n\n")
        elif escolha == "4":
            break
        else:
            print("Escolha um número existente.")

def main():
    menu()

if __name__ == "__main__":
    main()