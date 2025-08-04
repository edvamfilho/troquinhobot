import os


def listar_estrutura(caminho, prefixo=""):
    arquivos = os.listdir(caminho)
    arquivos.sort()
    for i, nome in enumerate(arquivos):
        caminho_completo = os.path.join(caminho, nome)
        marcador = "└── " if i == len(arquivos) - 1 else "├── "
        print(f"{prefixo}{marcador}{nome}")
        if os.path.isdir(caminho_completo):
            novo_prefixo = prefixo + \
                ("    " if i == len(arquivos) - 1 else "│   ")
            listar_estrutura(caminho_completo, novo_prefixo)


if __name__ == "__main__":
    raiz = "."  # ou altere para outro caminho, se quiser
    print("📁 Estrutura do Projeto TroquinhoBot:\n")
    listar_estrutura(raiz)
