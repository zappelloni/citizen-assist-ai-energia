# Citizen Assist AI – Energia (SERS)

Contribuição de **Soluções em Energias Renováveis e Sustentáveis** ao Citizen Assist AI, o assistente de terminal em Python que orienta jovens no primeiro emprego. Esta versão adiciona um **módulo de energia** que ajuda o jovem e a família a gastar menos com o banho de chuveiro elétrico, comparando economia de hábito com duas fontes renováveis (solar térmica e solar fotovoltaica), sempre com fontes, premissas e limitações.

Global Solution 2026.2 – Soluções em Energias Renováveis e Sustentáveis (FIAP – 1CCPK)

> **O que é de SERS neste repositório:** `energia.py`, `data/energia.json`, `data/comparacao_energia.csv`, a categoria **Energia** (orientações 14 a 18) em `data/base_conhecimento.json`, a opção **5** do menu e a pasta `docs/`. O restante (menu, busca, histórico, indicadores) veio da GS de Python e foi reaproveitado.

## Integrantes

| Nome | RM |
|---|---|
| Gabriel Rodrigues Zappelloni | 572060 |
| Felipe Pereira Restivo | 570712 |
| Maykon de Lima Silva | 574022 |

## Público e problema

**Público:** jovens de 14 a 24 anos que estão entrando no mercado de trabalho e, muitas vezes, começam a ajudar a pagar as contas da casa onde moram com a família.

**Necessidade energética:** a conta de luz pesa no orçamento dessas famílias, e o **chuveiro elétrico** costuma ser o aparelho que mais gasta (alta potência, uso diário por todos, concentrado no horário de pico das 18h às 21h). A pessoa não sabe quanto o banho custa, nem se vale mais a pena mudar o hábito, instalar aquecedor solar ou colocar painel solar, nem se a família tem direito à Tarifa Social.

**Como o assistente ajuda:** mostra, em linguagem simples, quanto o banho gasta, quanto cada alternativa economiza, quanto custa e em quanto tempo se paga, e deixa a pessoa simular a própria casa sem informar nenhum dado pessoal.

## Funcionalidades de energia

1. **Menu 5 – Energia: conta de luz e banho**
   - `1` Análise da casa de referência (4 pessoas, banho de 10 min, chuveiro de 5.500 W, Enel SP)
   - `2` Simular a minha casa (pessoas, minutos de banho, potência do chuveiro e meta de minutos; só números)
   - `3` Recomendações e limitações
   - `4` Dados, fontes e premissas (cada valor marcado como **REAL** ou **ESTIMADO**, com a fonte)
   - Depois de cada tela o assistente pergunta se foi útil e registra no histórico (origem `energia`), que entra nos indicadores (menu 3).
2. **Categoria Energia na busca e na navegação** (orientações 14 a 18): economizar no banho, Tarifa Social, aquecedor solar, fotovoltaica no telhado e como entender a conta de luz. Ex.: "chuveiro gasta muita luz", "tarifa social", "placa solar".
3. **`python energia.py`**: refaz todos os cálculos a partir de `data/energia.json` e gera `data/comparacao_energia.csv`.

## Como executar

Requisitos: Python 3.8 ou mais novo. Não usa bibliotecas externas.

```bash
git clone https://github.com/zappelloni/citizen-assist-ai-energia.git
cd citizen-assist-ai-energia
python main.py          # assistente completo (opção 5 = energia)
python energia.py       # só a análise de energia + CSV
```

No Windows também dá para dar duplo clique em `Iniciar Citizen Assist.bat`.

## Estrutura

```
citizen-assist-ai-energia/
├── README.md
├── main.py                    # menu (opção 5 = energia)
├── energia.py                 # SERS: CalculadoraEnergia + menu de energia
├── assistente.py / base_conhecimento.py / orientacao.py   # base da GS de Python
├── data/
│   ├── energia.json               # SERS: dados, unidades, fontes e premissas
│   ├── comparacao_energia.csv     # SERS: resultado da comparação (gerado)
│   ├── base_conhecimento.json     # 18 orientações (14 a 18 = Energia)
│   ├── historico.json / avaliacoes.json
└── docs/
    ├── ANALISE_ENERGIA.md         # cálculos passo a passo e justificativas
    ├── TESTES_USUARIOS.md         # roteiro e registro dos testes com usuários
    └── ROTEIRO_VIDEO.md           # roteiro do vídeo de até 3 minutos
```

## Resumo da análise (casa de referência, 1 ano)

Necessidade comum: **aquecer a água do banho de uma família de 4 pessoas em São Paulo (Enel SP) durante 1 ano.** Cálculos completos em [docs/ANALISE_ENERGIA.md](docs/ANALISE_ENERGIA.md).

| Alternativa | Tipo | Energia da rede no banho | Custo/ano | Economia/ano | Investimento | Retorno | CO2 evitado |
|---|---|---|---|---|---|---|---|
| Situação atual (10 min) | – | 1.338 kWh | R$ 1.372 | – | – | – | – |
| A) Banho de 6 min | Eficiência (hábito) | 803 kWh | R$ 823 | R$ 549 | R$ 0 | imediato | 13 kg |
| B) Aquecedor solar de água | Renovável (solar térmica) | 402 kWh | R$ 412 | R$ 960 | R$ 4.500 | ~4,7 anos | 23 kg |
| C) Fotovoltaica 2 kWp | Renovável (solar elétrica) | 0 kWh (compensada) | R$ 206 | R$ 1.166 | R$ 5.512 | ~4,7 anos | 33 kg |

A alternativa A também economiza cerca de **23 mil litros de água por ano**.

## Recomendações e justificativas

1. **Primeiro, o banho mais curto (A).** Custo zero, vale para quem mora de aluguel, economiza energia e água e alivia a rede no horário de pico. É a única alternativa viável para todo o público.
2. **Tarifa Social para quem tem direito.** Famílias no CadÚnico com renda de até meio salário mínimo por pessoa (ou com BPC) não pagam os primeiros 80 kWh do mês desde julho de 2025.
3. **Casa própria com telhado ensolarado: B ou C, junto com A.** As duas se pagam em cerca de 5 anos na casa de referência.
   - **Aquecedor solar (B):** menor entrada, resolve diretamente o banho e não depende de regras da distribuidora; vida útil menor (boiler 10 a 15 anos).
   - **Fotovoltaica (C):** entrada maior, vida útil maior (~25 anos) e a sobra do kit mínimo abate o resto da conta; depende de homologação e da Lei 14.300/2022.
4. **Impacto ambiental:** a eletricidade do Brasil já é muito renovável (fator do SIN de ~0,025 kg CO2/kWh em 2025), então o CO2 evitado é pequeno (13 a 33 kg/ano). Os ganhos ambientais mais relevantes são a **água economizada** (A), a **menor demanda no horário de pico** (A e B; a fotovoltaica gera de dia e não alivia o pico das 18h às 21h) e o menor uso de usinas térmicas nos momentos críticos. Do lado negativo, B e C exigem fabricação de equipamentos e descarte no fim da vida útil (vidro, metais, módulos).

## Limitações

- São **estimativas** para uma casa de referência, não resultados garantidos. Premissas marcadas como ESTIMADO em `data/energia.json` (fração solar de 70%, sol de 4,5 kWh/m²/dia, PIS/COFINS de 5%, custo de instalação de 30%, valor do crédito de 85% da tarifa, vazão de 4 L/min).
- A tarifa é da Enel SP (B1 residencial, bandeira verde); outras distribuidoras, bandeiras e o mês mudam o valor.
- Preços de equipamentos variam muito por região e fornecedor; o preço do kit fotovoltaico é de jan/2024. O custo do aquecedor solar foi tratado como fixo, mas cresce com o número de pessoas.
- Não considera manutenção, financiamento, inflação nem reajustes de tarifa (que tenderiam a encurtar o retorno).
- B e C exigem telhado com sol, obra e, no aluguel, autorização do proprietário.
- O fator de emissão usado é a média de jan-abr/2025 e varia mês a mês.

## Referências

- ANEEL – REH nº 3.596/2026, tarifa Enel SP (TUSD R$ 472,42/MWh + TE R$ 316,96/MWh), resumo em https://calculakwh.com.br/artigos/valor-do-kwh-enel-sp/ (acesso em 09/11/2026)
- ANEEL – Tarifa Social de Energia Elétrica: https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-social
- ANEEL – Bandeiras tarifárias: https://www.gov.br/aneel/pt-br/assuntos/tarifas/bandeiras-tarifarias
- IDEC – Economia com aquecedor solar (17/04/2025): https://idec.org.br/dicas-e-direitos/economia-com-aquecedor-solar
- Canal Solar / Greener – Valor da energia solar: https://canalsolar.com.br/valor-da-energia-solar/
- Canal Solar – Fator de emissão do SIN (MCTI), 2025: https://canalsolar.com.br/emissoes-de-co%e2%82%82-geracao-eletrica-mcti/
- Lei 14.300/2022 (geração distribuída): https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm
- Lei Complementar 194/2022 (ICMS sobre energia): https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp194.htm
- CRESESB – SunData (irradiação solar por localidade): https://cresesb.cepel.br/index.php?section=sundata
- Infomoney – Reajuste Enel SP 2026 (30/06/2026): https://www.infomoney.com.br/minhas-financas/aneel-aprova-alta-media-de-1018-para-tarifas-dos-consumidores-da-enel-sao-paulo/

## Testes com usuários

Roteiro, registro e ajustes em [docs/TESTES_USUARIOS.md](docs/TESTES_USUARIOS.md).

Teste feito em 09/11/2026 com **2 pessoas de fora da equipe**. Nenhum nome ou dado pessoal foi registrado; só os números da simulação (pessoas, minutos e potência), que ficam em `data/historico.json`.

| Pessoa | Situação testada | Casa simulada | Útil? | Tempo | Comentário |
|---|---|---|---|---|---|
| Pessoa 1 | Simular a própria casa (menu 5 > 2) | 3 pessoas, banho de 8 min, 5.500 W, meta de 5 min | Sim | 36,8 s | "Achou simples." |
| Pessoa 2 | Simular a própria casa (menu 5 > 2) | 2 pessoas, banho de 10 min, 5.500 W, meta de 6 min | Sim | 13,6 s | "Achou bem prático e rápido." |

| Indicador (menu 3) | Resultado |
|---|---|
| Atendimentos de energia | 2 |
| Orientação útil e compreendida | 100% (2 de 2) |
| Tempo médio | 25,2 s |
| Facilidade de uso (1 a 5) | 5,0 (notas 5 e 5) |

**O que o teste mostrou:** as duas casas eram menores que a casa de referência (2 e 3 pessoas em vez de 4). Com menos gasto no banho, as alternativas solares levariam **7,8 a 9,5 anos** para se pagar nessas casas, e não ~4,7 anos. Mas a recomendação da opção 3 era fixa ("se pagam em cerca de 5 anos") e não valia para elas.

**Ajuste feito:** depois de cada simulação, o assistente agora mostra uma **"Recomendação para a sua casa"** calculada com o retorno daquela casa (função `recomendacao_personalizada()` em `energia.py`): até 5 anos, sugere pedir orçamento; de 5 a 8, comparar com calma; acima de 8, focar no banho curto e na Tarifa Social. Para a Pessoa 2, por exemplo, ele passa a dizer que as solares levariam cerca de 9,4 anos e que o melhor caminho é o banho de 6 min (cerca de R$ 23/mês de economia).


## Vídeo técnico

Link (YouTube, não listado): https://youtu.be/LaNFusDtO8I
