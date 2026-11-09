# main.py
# Citizen Assist AI - Orientação para jovens no primeiro emprego
# + contribuição de Energias Renováveis e Sustentáveis (SERS): opção 5 e categoria Energia
# Execute com: python main.py

import os

from base_conhecimento import BaseConhecimento
from assistente import Assistente
from energia import menu_energia

# Garante que os caminhos "data/..." funcionem de qualquer pasta
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():   # lê o JSON e cria os objetos Orientacao
        print("Não foi possível carregar a base de conhecimento. Verifique o arquivo e tente de novo.")
        return

    assistente = Assistente("Citizen Assist AI", base)

    print("=" * 60)
    print(f"  {assistente.nome} - Primeiro Emprego")
    print("  Orientações sobre documentos, trabalho e energia para jovens")
    print("  Aviso: este assistente NÃO é um canal oficial.")
    print("  Nunca digite nome, CPF, telefone ou e-mail.")
    print("=" * 60)
    print(f"{len(base.orientacoes)} orientações carregadas em "
          f"{len(base.categorias())} categorias.")

    while True:
        print("\n===== MENU =====")
        print("1. Fazer uma pergunta")
        print("2. Navegar por categorias")
        print("3. Ver indicadores")
        print("4. Exportar atendimentos (CSV)")
        print("5. Energia: conta de luz e banho (SERS)")
        print("0. Sair")
        opcao = assistente.ler_opcao("Escolha: ", 0, 5)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        elif opcao == 5:
            menu_energia(assistente)
        else:
            assistente.avaliar()
            assistente.exportar_csv()
            print("Até logo!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
