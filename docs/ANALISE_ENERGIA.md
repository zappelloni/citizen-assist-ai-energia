# Análise de energia – banho com chuveiro elétrico

Contribuição de SERS ao Citizen Assist AI. Todos os números abaixo são calculados por `energia.py` a partir de `data/energia.json`; mudando uma premissa no JSON e rodando `python energia.py`, a tabela e o assistente se atualizam juntos.

## 1. Contexto

- **Público:** jovens de 14 a 24 anos no primeiro emprego, que moram com a família e passam a dividir as contas da casa.
- **Necessidade:** aquecer a água do banho da família, hoje feito com chuveiro elétrico.
- **Por que o chuveiro:** é um aparelho de alta potência (5.500 W a 7.500 W), usado todo dia por todos e concentrado entre 18h e 21h, quando a rede está mais carregada. Reduzir esse consumo dá retorno no bolso sem perder conforto essencial.
- **Período de referência:** 1 ano (365 dias), igual para todas as alternativas.
- **Local de referência:** cidade de São Paulo, distribuidora Enel SP, residencial B1.

## 2. Dados e premissas

| Premissa | Valor | Tipo | Origem |
|---|---|---|---|
| Pessoas na casa | 4 | Estimado | Família típica do público |
| Potência do chuveiro | 5.500 W | Real | IDEC (exemplo de chuveiro de 5.500 W) |
| Banho atual | 10 min/pessoa/dia | Estimado | Ponto de partida; o usuário informa o seu |
| Meta de banho | 6 min/pessoa/dia | Estimado | Redução de 4 min sem trocar equipamento |
| Vazão do chuveiro | 4 L/min | Estimado | Chuveiros elétricos ficam entre ~3 e 6 L/min |
| Tarifa sem tributos | R$ 0,78938/kWh | Real | ANEEL REH 3.596/2026, Enel SP B1, 04/07/2026 a 03/07/2027 |
| ICMS | 18% | Real | Teto da LC 194/2022 (SP) |
| PIS/COFINS | 5% | Estimado | Varia mês a mês (~1% a 7%) |
| Aquecedor solar – investimento | R$ 4.500 | Estimado | Meio da faixa R$ 3.000–6.000 (IDEC) |
| Aquecedor solar – fração solar | 70% | Estimado | Parte do aquecimento feita pelo sol |
| Aquecedor solar – vida útil | 15 anos | Real | IDEC: coletor 15–25 anos, boiler 10–15 anos |
| Fotovoltaica – preço do kit | R$ 2,12/Wp | Real | Greener via Canal Solar: kit 2 kWp por R$ 4.240 (jan/2024) |
| Fotovoltaica – kit mínimo | 2 kWp | Real | Faixa de kits residenciais começa em 2 kWp |
| Fotovoltaica – instalação | +30% sobre o kit | Estimado | Mão de obra, projeto e homologação |
| Horas de sol pleno (SP) | 4,5 kWh/m²/dia | Estimado | Brasil ~5,15 (Atlas Brasileiro); SP abaixo da média; conferir no CRESESB |
| Rendimento do sistema FV | 75% | Estimado | Perdas de calor, sujeira, cabos e inversor |
| Valor do crédito FV | 85% da tarifa | Estimado | Lei 14.300/2022: pagamento parcial do Fio B |
| Vida útil FV | 25 anos | Estimado | Garantia de desempenho usual dos módulos |
| Fator de emissão do SIN | 0,0247 kg CO2/kWh | Real | MCTI, média jan–abr/2025 (23,7; 24,8; 21,5; 28,9 kg/MWh) |

## 3. Cálculos

### 3.1 Tarifa final

Os tributos são cobrados "por dentro":

```
tarifa final = 0,78938 / (1 − 0,18 − 0,05) = 0,78938 / 0,77 ≈ R$ 1,025/kWh
```

### 3.2 Consumo atual do banho

Energia = potência × tempo.

```
tempo por dia = 4 pessoas × 10 min = 40 min = 0,667 h
energia por dia = 5,5 kW × 0,667 h = 3,67 kWh
energia por ano = 3,67 × 365 ≈ 1.338 kWh
custo por ano = 1.338 × 1,025 ≈ R$ 1.372 (≈ R$ 114/mês)
```

### 3.3 Alternativa A – banho de 6 minutos (eficiência)

```
energia = 5,5 kW × (4 × 6 / 60) h × 365 = 803 kWh/ano
economia = (1.338 − 803) × 1,025 ≈ R$ 549/ano (≈ R$ 46/mês)
água economizada = 4 pessoas × 4 min × 4 L/min × 365 = 23.360 L/ano
investimento = R$ 0
```

### 3.4 Alternativa B – aquecedor solar de água (renovável, solar térmica)

O sol cobre 70% do aquecimento; o chuveiro elétrico fica como apoio.

```
energia da rede = 1.338 × (1 − 0,70) ≈ 402 kWh/ano
economia = (1.338 − 402) × 1,025 ≈ R$ 960/ano (≈ R$ 80/mês)
retorno simples = 4.500 / 960 ≈ 4,7 anos
saldo em 15 anos = 960 × 15 − 4.500 ≈ R$ 9.906
```

O retorno de 4,7 anos fica dentro da faixa de 2 a 7 anos citada pelo IDEC, o que confere coerência às premissas.

### 3.5 Alternativa C – fotovoltaica (renovável, solar elétrica)

Potência necessária para gerar a energia do banho:

```
kWp = 1.338 / (4,5 × 0,75 × 365) ≈ 1,09 kWp
```

Como o menor kit residencial comum é de 2 kWp, a família compraria 2 kWp:

```
investimento = 2.000 Wp × R$ 2,12 × 1,30 ≈ R$ 5.512
geração do kit de 2 kWp = 2 × 4,5 × 0,75 × 365 ≈ 2.464 kWh/ano
economia (só a energia do banho, para comparar a mesma necessidade)
  = 1.338 × 1,025 × 0,85 ≈ R$ 1.166/ano (≈ R$ 97/mês)
retorno simples = 5.512 / 1.166 ≈ 4,7 anos
saldo em 25 anos = 1.166 × 25 − 5.512 ≈ R$ 23.643
```

A sobra (cerca de 1.125 kWh/ano) pode abater o resto da conta da casa, mas não foi somada para a comparação continuar justa.

### 3.6 Impacto ambiental (CO2)

```
CO2 evitado = energia que deixa de vir da rede × 0,0247 kg/kWh
A: 535 kWh × 0,0247 ≈ 13 kg/ano
B: 937 kWh × 0,0247 ≈ 23 kg/ano
C: 1.338 kWh × 0,0247 ≈ 33 kg/ano
```

## 4. Comparação

| | A) Banho 6 min | B) Aquecedor solar | C) Fotovoltaica 2 kWp |
|---|---|---|---|
| Economia por ano | R$ 549 | R$ 960 | R$ 1.166 |
| Investimento | R$ 0 | R$ 4.500 | R$ 5.512 |
| Retorno simples | imediato | ~4,7 anos | ~4,7 anos |
| Saldo na vida útil | – | R$ 9.906 (15 anos) | R$ 23.643 (25 anos) |
| CO2 evitado | 13 kg/ano | 23 kg/ano | 33 kg/ano |
| Água | −23.360 L/ano | igual | igual |
| Funciona no aluguel? | Sim | Só com autorização e obra | Só com autorização e homologação |
| Depende de regras externas? | Não | Não | Sim (Lei 14.300, distribuidora) |
| Conforto | Banho mais curto | Mantém (apoio elétrico) | Mantém |

### Viabilidade

- **A** é viável para 100% do público e começa a dar resultado no primeiro mês. O limite é o hábito: depende de a família manter a meta.
- **B** é viável para casas próprias com telhado ensolarado, caixa d'água e espaço para o boiler. Tem menor entrada que C e resolve diretamente o problema do banho.
- **C** é viável para casas próprias com telhado ensolarado e dinheiro (ou financiamento) para a entrada maior. Tem vida útil mais longa e flexibilidade (a energia serve para qualquer aparelho), mas o valor do crédito depende da regulação.

### Impactos ambientais além do CO2

- A matriz elétrica brasileira já é muito renovável, por isso o CO2 evitado é pequeno. Isso é um resultado da análise, não um defeito: o argumento ambiental mais forte aqui é **água** (A) e **pico de demanda**: A e B reduzem o consumo do chuveiro entre 18h e 21h. C não alivia o pico, porque gera durante o dia e compensa à noite por créditos; o chuveiro continua puxando 5,5 kW da rede na hora do banho.
- B e C exigem fabricação de equipamentos (vidro, alumínio, cobre, silício) e descarte correto no fim da vida útil.

## 5. Recomendação final (o que o assistente responde)

1. Começar pelo banho mais curto (A).
2. Verificar a Tarifa Social (até 80 kWh/mês gratuitos para quem tem direito; na tarifa estimada, até cerca de R$ 82/mês).
3. Casa própria: aquecedor solar (B) se o objetivo é o banho e a entrada precisa ser menor; fotovoltaica (C) se a família quer abater a conta toda e consegue a entrada maior. Sempre junto com A.

## 6. Limitações

Veja a seção Limitações do README. Em resumo: estimativas, uma distribuidora, preços que variam, sem manutenção, financiamento ou reajustes, e premissas marcadas como ESTIMADO que devem ser conferidas para cada casa.
