# energia.py
# Contribuição de Soluções em Energias Renováveis e Sustentáveis (SERS)
# ao Citizen Assist AI.
#
# Necessidade estudada: o banho com chuveiro elétrico, que costuma ser o
# maior gasto de energia da casa de uma família de baixa e média renda.
# Compara, para a MESMA necessidade (água quente do banho da família) e o
# MESMO período (1 ano):
#   A) Banho mais curto (eficiência, custo zero)
#   B) Aquecedor solar de água (renovável - solar térmica)
#   C) Painel solar fotovoltaico dimensionado para o chuveiro (renovável - solar elétrica)
#
# Rode sozinho para ver a análise da casa de referência e gerar o CSV:
#     python energia.py

import csv
import json
import os
import time

DIAS_ANO = 365
CAMINHO_DADOS = "data/energia.json"
CAMINHO_CSV = "data/comparacao_energia.csv"

AVISO = ("Os valores são ESTIMATIVAS com as premissas mostradas, não resultados "
         "garantidos. A conta real depende do aparelho, do clima, da tarifa do mês, "
         "da bandeira tarifária e dos hábitos da casa.")


def moeda(valor):
    """Formata em reais no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def numero(valor, casas=0):
    texto = f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return texto


class CalculadoraEnergia:
    def __init__(self, caminho=CAMINHO_DADOS):
        self.caminho = caminho
        self.dados = {}

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                self.dados = json.load(arquivo)
            return True
        except FileNotFoundError:
            print(f"Erro: {self.caminho} não encontrado.")
        except json.JSONDecodeError:
            print(f"Erro: {self.caminho} está corrompido.")
        return False

    def v(self, grupo, chave):
        """Atalho para ler o 'valor' de uma premissa."""
        return self.dados[grupo][chave]["valor"]

    # ------------------------------------------------------------------
    # Cálculos básicos
    # ------------------------------------------------------------------
    def tarifa_final(self):
        """Tarifa com tributos 'por dentro': T / (1 - ICMS - PIS/COFINS)."""
        t = self.v("tarifa", "sem_tributos_r_kwh")
        return t / (1 - self.v("tarifa", "icms") - self.v("tarifa", "pis_cofins"))

    @staticmethod
    def energia_banho_kwh_ano(potencia_w, pessoas, minutos):
        """E (kWh) = P (kW) x t (h). Por ano: P x (pessoas x minutos / 60) x 365."""
        horas_dia = pessoas * minutos / 60
        return potencia_w / 1000 * horas_dia * DIAS_ANO

    def kwp_para(self, kwh_ano):
        """Potência fotovoltaica para gerar kwh_ano:
        kWp = E / (horas de sol pleno x rendimento x 365)."""
        return kwh_ano / (self.v("fotovoltaica", "horas_sol_pleno")
                          * self.v("fotovoltaica", "rendimento_sistema") * DIAS_ANO)

    # ------------------------------------------------------------------
    # Comparação das alternativas
    # ------------------------------------------------------------------
    def comparar(self, pessoas=None, minutos=None, potencia_w=None, minutos_meta=None):
        casa = self.dados["casa_referencia"]
        pessoas = pessoas or casa["pessoas"]["valor"]
        minutos = minutos or casa["minutos_banho_atual"]["valor"]
        potencia_w = potencia_w or casa["potencia_chuveiro_w"]["valor"]
        if minutos_meta is None:
            minutos_meta = min(casa["minutos_banho_meta"]["valor"], minutos)

        tarifa = self.tarifa_final()
        fator = self.v("emissao", "fator_sin_kg_kwh")
        vazao = casa["vazao_chuveiro_l_min"]["valor"]

        e_atual = self.energia_banho_kwh_ano(potencia_w, pessoas, minutos)
        custo_atual = e_atual * tarifa

        # A) Banho mais curto
        e_a = self.energia_banho_kwh_ano(potencia_w, pessoas, minutos_meta)
        agua_a = pessoas * (minutos - minutos_meta) * vazao * DIAS_ANO

        # B) Aquecedor solar de água: o sol cobre parte do aquecimento
        fracao = self.v("aquecedor_solar", "fracao_solar")
        e_b = e_atual * (1 - fracao)
        invest_b = self.v("aquecedor_solar", "investimento_r")
        vida_b = self.v("aquecedor_solar", "vida_util_anos")

        # C) Fotovoltaica dimensionada para gerar a energia do chuveiro
        kwp = self.kwp_para(e_atual)
        # Não existe kit muito pequeno: compra-se pelo menos o kit mínimo
        kwp_comprado = max(kwp, self.v("fotovoltaica", "potencia_minima_kwp"))
        invest_c = (kwp_comprado * 1000 * self.v("fotovoltaica", "custo_kit_r_wp")
                    * (1 + self.v("fotovoltaica", "acrescimo_instalacao")))
        vida_c = self.v("fotovoltaica", "vida_util_anos")
        # O chuveiro continua gastando a mesma energia, mas ela é compensada
        # por créditos que valem só uma parte da tarifa (Lei 14.300).
        # Para comparar a MESMA necessidade, só a energia do banho entra na
        # economia; a sobra do kit mínimo é um benefício extra, não contado.
        economia_c = e_atual * tarifa * self.v("fotovoltaica", "valor_compensado")

        alternativas = [
            {"alternativa": "Situação atual", "tipo": "-",
             "energia_rede_kwh_ano": e_atual, "custo_ano": custo_atual,
             "economia_ano": 0, "investimento": 0, "vida_util_anos": None,
             "agua_economizada_l_ano": 0},
            {"alternativa": f"A) Banho de {minutos_meta} min", "tipo": "Eficiência (hábito)",
             "energia_rede_kwh_ano": e_a, "custo_ano": e_a * tarifa,
             "economia_ano": custo_atual - e_a * tarifa, "investimento": 0,
             "vida_util_anos": None, "agua_economizada_l_ano": agua_a},
            {"alternativa": "B) Aquecedor solar de água", "tipo": "Renovável (solar térmica)",
             "energia_rede_kwh_ano": e_b, "custo_ano": e_b * tarifa,
             "economia_ano": custo_atual - e_b * tarifa, "investimento": invest_b,
             "vida_util_anos": vida_b, "agua_economizada_l_ano": 0},
            {"alternativa": f"C) Fotovoltaica {numero(kwp_comprado, 1)} kWp", "tipo": "Renovável (solar elétrica)",
             "energia_rede_kwh_ano": 0, "custo_ano": custo_atual - economia_c,
             "economia_ano": economia_c, "investimento": invest_c,
             "vida_util_anos": vida_c, "agua_economizada_l_ano": 0},
        ]

        for alt in alternativas:
            evitado = e_atual - alt["energia_rede_kwh_ano"]
            alt["co2_evitado_kg_ano"] = evitado * fator
            if alt["investimento"] > 0 and alt["economia_ano"] > 0:
                alt["payback_anos"] = alt["investimento"] / alt["economia_ano"]
                alt["saldo_vida_util"] = (alt["economia_ano"] * alt["vida_util_anos"]
                                          - alt["investimento"])
            else:
                alt["payback_anos"] = 0 if alt["investimento"] == 0 else None
                alt["saldo_vida_util"] = None

        return {"pessoas": pessoas, "minutos": minutos, "minutos_meta": minutos_meta,
                "potencia_w": potencia_w, "tarifa": tarifa, "kwp": kwp,
                "kwp_comprado": kwp_comprado,
                "alternativas": alternativas}

    # ------------------------------------------------------------------
    # Saída
    # ------------------------------------------------------------------
    def exibir(self, resultado):
        r = resultado
        print()
        print("=== Banho com chuveiro elétrico: comparação em 1 ano ===")
        print(f"Casa: {r['pessoas']} pessoas, banho de {r['minutos']} min, "
              f"chuveiro de {numero(r['potencia_w'])} W")
        print(f"Tarifa usada: {moeda(r['tarifa'])}/kWh (Enel SP com tributos estimados)")
        print("Conta: energia (kWh) = potência (kW) x tempo (h)")
        print()
        for alt in r["alternativas"]:
            print(f">> {alt['alternativa']}  [{alt['tipo']}]")
            print(f"   Energia da rede no banho: {numero(alt['energia_rede_kwh_ano'])} kWh/ano"
                  f" | Custo: {moeda(alt['custo_ano'])}/ano")
            if alt["economia_ano"] > 0:
                print(f"   Economia: {moeda(alt['economia_ano'])}/ano"
                      f" ({moeda(alt['economia_ano'] / 12)}/mês)")
                print(f"   Investimento: {moeda(alt['investimento'])}", end="")
                if alt["payback_anos"]:
                    print(f" | Se paga em cerca de {numero(alt['payback_anos'], 1)} anos"
                          f" | Saldo em {alt['vida_util_anos']} anos: {moeda(alt['saldo_vida_util'])}")
                else:
                    print()
                print(f"   CO2 evitado: {numero(alt['co2_evitado_kg_ano'], 1)} kg/ano", end="")
                if alt["agua_economizada_l_ano"]:
                    print(f" | Água economizada: {numero(alt['agua_economizada_l_ano'])} L/ano")
                else:
                    print()
        if r["kwp_comprado"] > r["kwp"]:
            print(f"Obs.: para o banho bastariam {numero(r['kwp'], 2)} kWp, mas o menor kit comum é de "
                  f"{numero(r['kwp_comprado'], 1)} kWp. A energia que sobra pode abater o resto da conta,")
            print("      mas não foi somada na economia para comparar só a necessidade do banho.")
        print()
        print("Aviso: " + AVISO)

    def exportar_csv(self, resultado, caminho=CAMINHO_CSV):
        campos = ["alternativa", "tipo", "energia_rede_kwh_ano", "custo_ano", "economia_ano",
                  "investimento", "payback_anos", "vida_util_anos", "saldo_vida_util",
                  "co2_evitado_kg_ano", "agua_economizada_l_ano"]
        try:
            with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
                escritor.writeheader()
                for alt in resultado["alternativas"]:
                    linha = {}
                    for c in campos:
                        valor = alt[c]
                        linha[c] = (f"{valor:.2f}".replace(".", ",")
                                    if isinstance(valor, float) else valor)
                    escritor.writerow(linha)
            print(f"Comparação salva em {caminho}")
        except OSError:
            print(f"Não foi possível salvar {caminho}. Ele está aberto em outro programa?")

    def exibir_premissas(self):
        print("\n=== Dados, fontes e premissas ===")
        for grupo, itens in self.dados.items():
            if not isinstance(itens, dict):
                continue
            for chave, p in itens.items():
                origem = p.get("fonte") or p.get("justificativa", "")
                marca = "REAL" if p["tipo"] == "real" else "ESTIMADO"
                print(f"- [{marca}] {grupo}.{chave} = {p['valor']} {p['unidade']}")
                print(f"    {origem}")
                if "url" in p:
                    print(f"    {p['url']}")
        print("\n" + AVISO)


# ----------------------------------------------------------------------
# Menu de energia usado pelo Citizen Assist AI (opção 5 do menu principal)
# ----------------------------------------------------------------------
RECOMENDACOES = """
=== O que recomendamos (nesta ordem) ===
1. Comece pelo banho mais curto (alternativa A). Não custa nada, vale para
   quem mora de aluguel e ainda economiza água. Na casa de referência,
   passar de 10 para 6 minutos economiza cerca de R$ 46 por mês.
2. Se a família tem direito, peça a Tarifa Social: quem está no CadÚnico com
   renda de até meio salário mínimo por pessoa (ou recebe BPC) não paga os
   primeiros 80 kWh do mês.
3. Casa própria com telhado ensolarado: as duas renováveis se pagam em
   cerca de 5 anos na casa de referência.
   - Aquecedor solar de água (B): precisa de menos dinheiro de entrada
     (cerca de R$ 4.500), resolve direto o banho e não depende das regras
     de compensação da distribuidora. Boiler dura de 10 a 15 anos.
   - Painel fotovoltaico (C): entrada maior (cerca de R$ 5.500 pelo kit
     mínimo de 2 kWp), dura mais (cerca de 25 anos) e a energia que sobra
     abate o resto da conta. Depende de homologação e da Lei 14.300.
   Junte a alternativa A com B ou C: banho curto reduz o tamanho (e o
   custo) do sistema que você precisa.

Limitações: são estimativas para uma casa de referência em São Paulo (Enel SP),
com premissas marcadas como ESTIMADO na opção 4. Preços de equipamentos variam:
peça pelo menos 3 orçamentos. Aquecedor solar e fotovoltaica exigem telhado com
sol, obra e, no aluguel, autorização do dono. No Brasil a eletricidade já é quase
toda renovável, então o ganho em CO2 é pequeno; o maior benefício é no bolso, na
água (alternativa A) e em aliviar a rede no horário de pico (banhos entre 18h e 21h), o que
vale para A e B; a fotovoltaica gera de dia e não alivia o pico.
"""


def recomendacao_personalizada(resultado):
    """Ajuste feito após o teste com usuários: casas menores gastam menos
    no banho, então as solares demoram mais para se pagar. A recomendação
    passa a depender do retorno calculado para a casa simulada."""
    alts = resultado["alternativas"]
    banho, solar, fv = alts[1], alts[2], alts[3]
    retorno = min(solar["payback_anos"] or 99, fv["payback_anos"] or 99)
    linhas = ["\n=== Recomendação para a sua casa ==="]
    if banho["economia_ano"] > 0:
        linhas.append(f"1. Banho de {resultado['minutos_meta']} min: economia de "
                      f"{moeda(banho['economia_ano'] / 12)}/mês sem gastar nada. Comece por aqui.")
    else:
        linhas.append("1. Seu banho já está no tempo da meta. Ótimo! Use a posição verão nos dias quentes.")
    if retorno <= 5:
        linhas.append(f"2. As solares se pagam em cerca de {numero(retorno, 1)} anos na sua casa: "
                      "vale pedir orçamento se a casa for própria e tiver telhado com sol.")
    elif retorno <= 8:
        linhas.append(f"2. As solares levariam cerca de {numero(retorno, 1)} anos para se pagar. "
                      "Pode valer a pena, mas compare orçamentos com calma.")
    else:
        linhas.append(f"2. Na sua casa as solares levariam cerca de {numero(retorno, 1)} anos para se pagar, "
                      "porque o gasto com banho é menor. Foque no banho curto e na Tarifa Social.")
    linhas.append("3. Veja se a família tem direito à Tarifa Social (opção 3 deste menu).")
    linhas.append("Lembre: são estimativas, não valores garantidos.")
    return "\n".join(linhas)


def ler_inteiro(mensagem, minimo, maximo):
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit() and minimo <= int(texto) <= maximo:
            return int(texto)
        print(f"Valor inválido. Digite um número de {minimo} a {maximo}.")


def menu_energia(assistente=None):
    calc = CalculadoraEnergia()
    if not calc.carregar():
        return
    while True:
        print("\n===== ENERGIA: CONTA DE LUZ E BANHO =====")
        print("1. Ver a análise da casa de referência")
        print("2. Simular a minha casa")
        print("3. Recomendações e limitações")
        print("4. Dados, fontes e premissas")
        print("0. Voltar")
        op = ler_inteiro("Escolha: ", 0, 4)
        inicio = time.time()
        if op == 0:
            return
        if op == 1:
            calc.exibir(calc.comparar())
            registro = "[energia] análise de referência"
        elif op == 2:
            print("\nResponda só com números. Não precisa informar nenhum dado pessoal.")
            pessoas = ler_inteiro("Quantas pessoas tomam banho na casa? (1 a 15): ", 1, 15)
            minutos = ler_inteiro("Quantos minutos dura cada banho, em média? (1 a 60): ", 1, 60)
            print("A potência fica na etiqueta ou no manual do chuveiro (ex.: 5500 W).")
            print("Se não souber, digite 0 que usamos 5500 W.")
            potencia = ler_inteiro("Potência do chuveiro em W (0, ou 2000 a 9000): ", 0, 9000)
            if 0 < potencia < 2000:
                print("Valor muito baixo para um chuveiro. Usando 5500 W.")
                potencia = 0
            meta = ler_inteiro(f"Quantos minutos você acha possível? (1 a {minutos}): ", 1, minutos)
            resultado = calc.comparar(pessoas, minutos, potencia or None, meta)
            calc.exibir(resultado)
            print(recomendacao_personalizada(resultado))
            registro = f"[energia] simulação {pessoas}p {minutos}min {potencia or 5500}W meta {meta}min"
        elif op == 3:
            print(RECOMENDACOES)
            registro = "[energia] recomendações"
        else:
            calc.exibir_premissas()
            registro = "[energia] fontes e premissas"

        if assistente is not None:
            ajudou = assistente.ler_sim_nao("Essa orientação foi útil e deu para entender? (s/n): ")
            assistente.registrar("energia", registro, None, True, ajudou, 1, inicio)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    calc = CalculadoraEnergia()
    if calc.carregar():
        res = calc.comparar()
        calc.exibir(res)
        calc.exportar_csv(res)
