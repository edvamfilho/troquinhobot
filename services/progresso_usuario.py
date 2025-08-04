from services.state_manager import (
    verificar_progresso,
    registrar_progresso,
    obter_flag,
    definir_flag,
)


def etapa_concluida(chat_id, etapa_nome: str) -> bool:
    """Verifica se uma etapa foi marcada como concluída"""
    return bool(verificar_progresso(chat_id, etapa_nome))


def marcar_etapa_concluida(chat_id, etapa_nome: str):
    """Marca uma etapa como concluída no progresso"""
    registrar_progresso(chat_id, etapa_nome, True)


def definir_nivel_conhecimento(chat_id, nivel: str):
    """Ex: Iniciante, Entusiasta, Experiente"""
    definir_flag(chat_id, "nivel_conhecimento", nivel)


def obter_nivel_conhecimento(chat_id):
    return obter_flag(chat_id, "nivel_conhecimento")


def definir_perfil_risco(chat_id, perfil: str):
    """Ex: Conservador, Moderado, Agressivo"""
    definir_flag(chat_id, "perfil_risco", perfil)


def obter_perfil_risco(chat_id):
    return obter_flag(chat_id, "perfil_risco")


def marcar_carteira_conectada(chat_id, conectada=True):
    definir_flag(chat_id, "carteira_conectada", conectada)


def carteira_esta_conectada(chat_id) -> bool:
    return bool(obter_flag(chat_id, "carteira_conectada"))


def pode_acessar(chat_id, recurso: str) -> bool:
    """Verifica se o usuário pode acessar certo recurso"""
    if recurso == "bot_trader":
        return carteira_esta_conectada(chat_id) and obter_perfil_risco(chat_id)
    if recurso == "estrategia_teste":
        return carteira_esta_conectada(chat_id)
    if recurso == "trilha_avancada":
        nivel = obter_nivel_conhecimento(chat_id)
        return nivel in ["Entusiasta", "Experiente"]
    return True
