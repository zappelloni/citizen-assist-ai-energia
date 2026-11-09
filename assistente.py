# assistente.py
# Classe Assistente: conversa com o cidadão, guarda o histórico e calcula os indicadores.

import csv
import json
import time
from datetime import datetime

from base_conhecimento import nivel_confianca, LIMITE_MEDIA

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_segundos"]


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_avaliacoes="data/avaliacoes.json"):
        self.nome = nome
        self.base = base                    # objeto BaseConhecimento (composição)
        self.caminho_historico = caminho_historico
        self.caminho_avaliacoes = caminho_avaliacoes
        self.historico = self._ler_lista_json(caminho_historico)
        self.avaliacoes = self._ler_lista_json(caminho_avaliacoes)

    # ------------------------------------------------------------------
    # Arquivos
    # ------------------------------------------------------------------
    def _ler_lista_json(self, caminho):
        """Lê uma lista de um arquivo JSON. Se não existir ou estiver
        corrompido, começa com uma lista vazia (o programa não trava)."""
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                return dados
            print(f"Aviso: {caminho} não tinha uma lista. Começando do zero.")
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print(f"Aviso: {caminho} estava corrompido. Começando do zero.")
        return []

    def _salvar_lista_json(self, caminho, lista):
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(lista, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print(f"Aviso: não foi possível salvar {caminho}.")

    # ------------------------------------------------------------------
    # Leitura segura do teclado (entradas inválidas nunca encerram o programa)
    # ------------------------------------------------------------------
    def ler_opcao(self, mensagem, minimo, maximo):
        while True:
            texto = input(mensagem).strip()
            if not texto.isdigit():
                print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")
                continue
            numero = int(texto)
            if minimo <= numero <= maximo:
                return numero
            print(f"Opção fora da faixa. Digite um número de {minimo} a {maximo}.")

    def ler_sim_nao(self, mensagem):
        while True:
            texto = input(mensagem).strip().lower()
            if texto in ("s", "sim"):
                return True
            if texto in ("n", "nao", "não"):
                return False
            print("Resposta inválida. Digite s ou n.")

    @staticmethod
    def tem_dado_pessoal(texto):
        """Recusa textos com 8 ou mais dígitos (CPF, telefone...) ou com @ (e-mail)."""
        digitos = sum(1 for c in texto if c.isdigit())
        return digitos >= 8 or "@" in texto

    # ------------------------------------------------------------------
    # Atendimento
    # ------------------------------------------------------------------
    def registrar(self, origem, pergunta, orientacao, encontrou, ajudou,
                  tentativas, inicio):
        """Salva um atendimento no histórico (data/historico.json)."""
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1),
        }
        self.historico.append(atendimento)
        self._salvar_lista_json(self.caminho_historico, self.historico)

    def perguntar(self):
        """Modo de perguntas em texto livre, com busca por pontuação."""
        print("\nPergunte em poucas palavras. Ex.: 'como tiro a carteira de trabalho?'")
        print("Não digite nome, CPF, telefone ou e-mail.")
        inicio = time.time()
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if pergunta == "":
                print("Você não digitou nada. Escreva sua dúvida ou 0 para voltar.")
                continue
            if self.tem_dado_pessoal(pergunta):
                # Não conta tentativa e NÃO é registrado
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            # Nenhuma orientação chegou a 3 pontos: "não encontrei"
            if not resultados or resultados[0][0] < LIMITE_MEDIA:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras (ex.: 'cpf', 'estágio', 'seguro desemprego')")
                print("ou veja as categorias: " + ", ".join(self.base.categorias()))
                self.registrar("pergunta", pergunta, None, False, False,
                               tentativas, inicio)
                continue

            pontos, melhor = resultados[0]
            print(f"\nConfiança da resposta: {nivel_confianca(pontos)} ({pontos} pontos)")
            melhor.exibir()

            # Até duas alternativas
            alternativas = [t for t in resultados[1:3] if t[0] >= LIMITE_MEDIA]
            if alternativas:
                print("Outras orientações parecidas:")
                for i, (pts, o) in enumerate(alternativas, start=1):
                    print(f"  {i}. {o.titulo} ({pts} pontos)")

            ajudou = self.ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
            mostrada = melhor

            if not ajudou and alternativas:
                escolha = self.ler_opcao(
                    f"Quer ver uma alternativa? (1 a {len(alternativas)}, 0 para não): ",
                    0, len(alternativas))
                if escolha != 0:
                    mostrada = alternativas[escolha - 1][1]
                    mostrada.exibir()
                    ajudou = self.ler_sim_nao("E essa, respondeu sua dúvida? (s/n): ")

            self.registrar("pergunta", pergunta, mostrada, True, ajudou,
                           tentativas, inicio)

            if ajudou:
                print("Que bom! Pode fazer outra pergunta.")
                inicio = time.time()   # começa um novo atendimento
                tentativas = 0
            else:
                print("Tente escrever de outro jeito ou use a navegação por categorias.")

    def navegar(self):
        """Navegação por categorias e orientações numeradas, com 0 para voltar."""
        while True:
            inicio = time.time()
            categorias = self.base.categorias()
            print("\n=== Categorias ===")
            for i, cat in enumerate(categorias, start=1):
                print(f"{i}. {cat}")
            print("0. Voltar")
            op = self.ler_opcao("Escolha uma categoria: ", 0, len(categorias))
            if op == 0:
                return

            categoria = categorias[op - 1]
            while True:
                orientacoes = self.base.por_categoria(categoria)
                print(f"\n=== {categoria} ===")
                for i, o in enumerate(orientacoes, start=1):
                    print(f"{i}. {o.titulo}")
                print("0. Voltar")
                op2 = self.ler_opcao("Escolha uma orientação: ", 0, len(orientacoes))
                if op2 == 0:
                    break
                escolhida = orientacoes[op2 - 1]
                escolhida.exibir()
                ajudou = self.ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", f"[{categoria}] {escolhida.titulo}",
                               escolhida, True, ajudou, 1, inicio)
                inicio = time.time()

    # ------------------------------------------------------------------
    # Indicadores e exportação
    # ------------------------------------------------------------------
    def avaliar(self):
        """Pede a nota de facilidade (1 a 5) ao sair."""
        nota = self.ler_opcao("\nDe 1 a 5, quão fácil foi usar o assistente? ", 1, 5)
        self.avaliacoes.append(nota)
        self._salvar_lista_json(self.caminho_avaliacoes, self.avaliacoes)
        print("Obrigado pela avaliação!")

    def indicadores(self, mostrar=True):
        """Calcula os indicadores a partir do histórico e mostra na tela."""
        total = len(self.historico)
        if total == 0:
            if mostrar:
                print("\nAinda não há atendimentos registrados.")
            return {}

        encontrados = [a for a in self.historico if a["encontrou"]]
        ajudou = [a for a in self.historico if a["ajudou"]]
        tempos = [a["tempo_segundos"] for a in ajudou]
        tentativas = [a["tentativas"] for a in self.historico]
        sem_solucao = [a["pergunta"] for a in self.historico if not a["ajudou"]]

        resultado = {
            "atendimentos": total,
            "encontrada_pct": round(len(encontrados) / total * 100, 1),
            "acerto_pct": round(len(ajudou) / total * 100, 1),
            "tempo_medio": round(sum(tempos) / len(tempos), 1) if tempos else 0,
            "tentativas_media": round(sum(tentativas) / total, 1),
            "facilidade": (round(sum(self.avaliacoes) / len(self.avaliacoes), 1)
                           if self.avaliacoes else None),
            "sem_solucao": sem_solucao,
        }

        if mostrar:
            print("\n=== Indicadores ===")
            print(f"Atendimentos registrados ....... {resultado['atendimentos']}")
            print(f"Resposta encontrada ............ {resultado['encontrada_pct']}%")
            print(f"Taxa de acerto (ajudou) ........ {resultado['acerto_pct']}%")
            print(f"Tempo médio para encontrar ..... {resultado['tempo_medio']} s")
            print(f"Tentativas por atendimento ..... {resultado['tentativas_media']}")
            fac = resultado["facilidade"]
            print(f"Facilidade de uso (1 a 5) ...... {fac if fac is not None else 'sem notas'}"
                  f" ({len(self.avaliacoes)} notas)")
            print("Dúvidas sem solução:")
            if sem_solucao:
                for p in sem_solucao:
                    print(f"  - {p}")
            else:
                print("  (nenhuma)")
        return resultado

    def exportar_csv(self, caminho="data/atendimentos.csv"):
        """Exporta o histórico para CSV usando csv.DictWriter."""
        try:
            with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV, delimiter=";")
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow(atendimento)
            print(f"\n{len(self.historico)} atendimentos exportados para {caminho}")
        except OSError:
            print(f"Não foi possível salvar {caminho}. Ele está aberto em outro programa?")
