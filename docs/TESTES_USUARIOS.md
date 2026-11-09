# Testes com usuários – módulo de energia

Objetivo: verificar se as orientações de energia são **compreendidas** e **úteis** para o público (jovens de 14 a 24 anos e suas famílias). Nenhum nome, CPF, telefone ou endereço é registrado: cada pessoa vira "Pessoa 1", "Pessoa 2"...

## Como aplicar (cerca de 10 minutos por pessoa)

1. Abrir `python main.py` e deixar a pessoa usar sozinha, sem explicar antes.
2. Pedir que ela faça estas situações, uma de cada vez:
   - **S1.** "Descubra quanto o banho da sua casa custa por ano." (menu 5 > 2)
   - **S2.** "Pergunte ao assistente como economizar na conta de luz." (menu 1, texto livre)
   - **S3.** "Descubra se a sua família poderia ter desconto na conta de luz." (Tarifa Social)
   - **S4.** "Vale mais a pena aquecedor solar ou placa solar? Por quê?" (menu 5 > 1 e 3)
3. Depois de cada situação, o próprio assistente pergunta se foi útil (fica no histórico). Anote também:
   - a pessoa conseguiu sozinha? (sim / com ajuda / não)
   - ela entendeu que os valores são estimativas? (pergunte: "esse valor é garantido?")
   - comentário dela, com as palavras dela
4. Ao sair, a pessoa dá a nota de facilidade (1 a 5).
5. Rodar o menu 3 (Indicadores) e copiar os números para a tabela de resultados.

## Registro (09/11/2026)

| Pessoa | Situação | Casa simulada | Conseguiu? | Útil? | Tempo | Comentário |
|---|---|---|---|---|---|---|
| Pessoa 1 | S1 – simular a própria casa | 3 pessoas, 8 min, 5.500 W, meta 5 min | Sim | Sim | 36,8 s | _(preencher)_ |
| Pessoa 2 | S1 – simular a própria casa | 2 pessoas, 10 min, 5.500 W, meta 6 min | Sim | Sim | 13,6 s | _(preencher)_ |

## Resultados (menu 3 – Indicadores)

| Indicador | Resultado |
|---|---|
| Pessoas testadas | 2 |
| Atendimentos | 2 |
| Útil / entendeu (ajudou) | 100% (2 de 2) |
| Tempo médio | 25,2 s |
| Facilidade de uso (1 a 5) | 5,0 (notas 5 e 5) |
| Dúvidas sem solução | nenhuma |

## Ajustes feitos depois do teste

| O que apareceu no teste | Ajuste feito | Onde |
|---|---|---|
| As duas casas testadas eram menores que a de referência; nelas as solares levariam 7,8 a 9,5 anos para se pagar, mas a recomendação fixa dizia "cerca de 5 anos". | Recomendação personalizada depois de cada simulação, calculada com o retorno daquela casa (até 5 anos: pedir orçamento; 5 a 8: comparar; acima de 8: focar no banho curto e na Tarifa Social). | `energia.py`, função `recomendacao_personalizada()` |
