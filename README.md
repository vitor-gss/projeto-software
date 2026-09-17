# Sistema de Alertas Meteorológicos Multifonte
Projeto para, a partir de dados climáticos, informar tipos de alerta diferentes para cada caso. Será gerado um relatório de monitoramento de várias cidades.

## Requisitos feitos
- **RF1 [E] — Dados climáticos protegidos**. Os dados climáticos obtidos da API jamais podem
existir em estado inválido ou inconsistente.
- **RF2 [E] — Calculado, não atribuível**. Código externo não pode alterar uma leitura climática
após a obtenção; valores derivados devem ser calculados.
- **RF3 [A/H] — Múltiplas categorias de alerta.** O sistema deve suportar pelo menos quatro
categorias distintas de alerta meteorológico, cada uma avaliando o perigo com critérios próprios
aplicados aos mesmos dados climáticos.
- **RF4 [P] — Alertas autodescritivos.** Cada categoria de alerta deve se descrever de forma
legível e apropriada ao seu tipo quando exibida em uma lista genérica.
- **RF5 [P] — Avaliação uniforme.** O sistema deve avaliar uma coleção mista de alertas e
produzir uma avaliação de risco para cada um, sem que a lógica de avaliação saiba qual
categoria específica está processando.
- **RF6 [A/IF] — Provedores de dados intercambiáveis**. O sistema deve poder trocar de
provedor de dados climáticos sem alterações na lógica de avaliação de alertas.
- **RF7 [C] — Monitoramento de múltiplas localidades.** O sistema deve monitorar várias
localidades e produzir um único relatório consolidado.

