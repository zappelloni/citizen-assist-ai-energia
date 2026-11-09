# base_conhecimento.py
# Classe BaseConhecimento: guarda todas as orientações e faz a busca.

import json
from orientacao import Orientacao

# Tabela de troca de letras acentuadas (dicionário)
ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# Campos que toda orientação precisa ter no JSON
CAMPOS = ("id", "categoria", "titulo", "palavras_chave", "resposta",
          "documentos", "onde", "fonte", "verificado_em")

# Pesos e limites da pontuação (podem ser ajustados aqui)
PONTOS_PALAVRA_CHAVE = 3
PONTOS_PALAVRA_TITULO = 1
TAMANHO_MINIMO_PALAVRA = 4
LIMITE_ALTA = 6
LIMITE_MEDIA = 3


def normalizar(texto):
    """Deixa o texto em minúsculas, sem acentos e sem pontuação.
    Devolve com um espaço no começo e no fim, para comparar palavras inteiras."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()-/":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


def nivel_confianca(pontos):
    """Transforma a pontuação em um nível de confiança."""
    if pontos >= LIMITE_ALTA:
        return "ALTA"
    if pontos >= LIMITE_MEDIA:
        return "MÉDIA"
    return "BAIXA"


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []  # lista de objetos Orientacao (composição)

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao.
        Devolve True se carregou alguma orientação, False se deu problema."""
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: o arquivo {self.caminho} não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: o arquivo {self.caminho} está corrompido (JSON inválido).")
            return False

        if not isinstance(dados, list):
            print("Erro: a base de conhecimento deve ser uma lista de orientações.")
            return False

        for registro in dados:
            # Pula registros incompletos em vez de travar o programa
            if not isinstance(registro, dict) or any(c not in registro for c in CAMPOS):
                print("Aviso: uma orientação incompleta foi ignorada.")
                continue
            self.orientacoes.append(Orientacao(**{c: registro[c] for c in CAMPOS}))

        return len(self.orientacoes) > 0

    def categorias(self):
        """Lista das categorias, sem repetir, na ordem em que aparecem."""
        lista = []
        for o in self.orientacoes:
            if o.categoria not in lista:
                lista.append(o.categoria)
        return lista

    def por_categoria(self, categoria):
        """Todas as orientações de uma categoria."""
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """Calcula os pontos de UMA orientação para a pergunta.
        +3 para cada palavra-chave que aparece na pergunta
        +1 para cada palavra da pergunta (4+ letras) que aparece no título"""
        pergunta_n = normalizar(pergunta)
        pontos = 0

        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta_n:
                pontos += PONTOS_PALAVRA_CHAVE

        palavras_titulo = normalizar(orientacao.titulo).split()
        palavras_ja_contadas = set()
        for palavra in pergunta_n.split():
            if (len(palavra) >= TAMANHO_MINIMO_PALAVRA
                    and palavra in palavras_titulo
                    and palavra not in palavras_ja_contadas):
                pontos += PONTOS_PALAVRA_TITULO
                palavras_ja_contadas.add(palavra)

        return pontos

    def buscar(self, pergunta):
        """Devolve uma lista de tuplas (pontos, orientacao),
        da maior para a menor pontuação. Só entra quem fez pelo menos 1 ponto."""
        resultados = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultados.append((pontos, o))
        resultados.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultados
