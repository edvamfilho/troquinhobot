import json
import os

CAMINHO_ESTADO = "data/usuarios.json"


def carregar_estado(chat_id):
    if not os.path.exists(CAMINHO_ESTADO):
        return {}

    with open(CAMINHO_ESTADO, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return dados.get(str(chat_id), {})


def salvar_estado(chat_id, estado):
    if not os.path.exists("data"):
        os.makedirs("data")

    dados = {}
    if os.path.exists(CAMINHO_ESTADO):
        with open(CAMINHO_ESTADO, "r", encoding="utf-8") as f:
            dados = json.load(f)

    dados[str(chat_id)] = estado

    with open(CAMINHO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def atualizar_estado(chat_id, novos_dados):
    estado_atual = carregar_estado(chat_id)
    estado_atual.update(novos_dados)
    salvar_estado(chat_id, estado_atual)


def obter_estado_usuario(chat_id):
    return carregar_estado(chat_id)


def limpar_estado(chat_id):
    if not os.path.exists(CAMINHO_ESTADO):
        return

    with open(CAMINHO_ESTADO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    if str(chat_id) in dados:
        del dados[str(chat_id)]

        with open(CAMINHO_ESTADO, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)


def criar_usuario(chat_id):
    if not os.path.exists(CAMINHO_ESTADO):
        with open(CAMINHO_ESTADO, "w", encoding="utf-8") as f:
            json.dump({}, f)
    if not carregar_estado(chat_id):
        salvar_estado(chat_id, {"etapa": "etapa1"})


def salvar_resposta_conhecimento(chat_id, pergunta_id, resposta):
    estado = carregar_estado(chat_id)
    respostas = estado.get("respostas_conhecimento", {})
    respostas[pergunta_id] = resposta
    estado["respostas_conhecimento"] = respostas
    salvar_estado(chat_id, estado)


def inferir_nivel_conhecimento(respostas: dict) -> str:
    """Simples lógica de inferência – pode ser refinada."""
    if not respostas:
        return "Desconhecido"

    tempo = respostas.get("tempo")
    exchanges = respostas.get("exchanges")
    tipo_operacao = respostas.get("tipo_operacao")

    if tempo == "Mais de 2 anos" and tipo_operacao in ["Fiz daytrade", "Faço swing trade"]:
        return "Avançado"
    elif tempo == "Entre 6 meses e 2 anos" or exchanges:
        return "Intermediário"
    else:
        return "Iniciante"


def salvar_resposta_risco(chat_id, pergunta_id, resposta):
    estado = carregar_estado(chat_id)
    respostas = estado.get("respostas_risco", {})
    respostas[pergunta_id] = resposta
    estado["respostas_risco"] = respostas
    salvar_estado(chat_id, estado)


def inferir_perfil_risco(chat_id) -> str:
    estado = carregar_estado(chat_id)
    respostas = estado.get("respostas_risco", {})
    if not respostas:
        return "Indefinido"

    conservador = sum(1 for r in respostas.values()
                      if "conservador" in r.lower())
    moderado = sum(1 for r in respostas.values() if "moderado" in r.lower())
    agressivo = sum(1 for r in respostas.values() if "agressivo" in r.lower())
    if conservador >= moderado and conservador >= agressivo:
        return "Conservador"
    elif moderado >= conservador and moderado >= agressivo:
        return "Moderado"
    else:
        return "Agressivo"
