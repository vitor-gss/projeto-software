import requests
from sistema import (AlertaTempestade, AlertaGeada, AlertaCalor, AlertaAlagamento)
from provedor import OpenMeteoProvider

cidades = [
    ## ("Nome", lat, lon)
    ##todas as cidades que queremos

    #RF6, apenas registrar as cidades para testes durante o desenvolvimento
]

alertas = [AlertaAlagamento(), AlertaTempestade(), AlertaGeada(), AlertaCalor()]

def main():
    #RF6, colocar a OPENMETEO na demonstração
    provedor = OpenMeteoProvider()

    for cidade,lat,lon in cidades:
        print(f"{cidade} :")
        try:
            leitura = provedor.obter_leitura(cidade, lat, lon)
        except ValueError as e:
            print(f" [dado invalido] {e}")
            continue

        #RF5 | falta colocar as opções (Ex.: 1 faz tal, 2 faz aquilo) como menu
        print(f"{leitura.temperatura}°C ; {leitura.umidade}% ; {leitura.chuva_mm_h}mm/h.")
        for alerta in alertas:
            nivel = alerta.avaliar_risco(leitura)
            #RF7, trocar o print e colocar para sair relatorio
            print(f"{alerta.nome} | {nivel.value}")

if __name__ == "__main__":
    main()