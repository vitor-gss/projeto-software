import requests
from sistema import (AlertaTempestade, AlertaGeada, AlertaCalor, AlertaAlagamento)
from provedor import OpenMeteoProvider

cidades = [
    ## ("Nome", lat, lon)
    ##todas as cidades que queremos
]

alertas = [AlertaAlagamento(), AlertaTempestade(), AlertaGeada(), AlertaCalor()]

def main():
    provedor = OpenMeteoProvider()

    for cidade,lat,lon in cidades:
        print(f"{cidade} :")
        try:
            leitura = provedor.obter_leitura(cidade, lat, lon)
        except ValueError as e:
            print(f" [dado invalido] {e}")
            continue

        print(f"{leitura.temperatura}°C ; {leitura.umidade}% ; {leitura.chuva_mm_h}mm/h.")
        for alerta in alertas:
            nivel = alerta.avaliar_risco(leitura)
            print(f"{alerta.nome} | {nivel.value}")

if __name__ == "__main__":
    main()