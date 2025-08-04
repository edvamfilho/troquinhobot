# utils/preset_manager.py

from content.configuracoes_default import PRESETS_POR_ESTILO


def buscar_preset_por_estilo(estilo: str) -> dict:
    """
    Retorna o preset padrão para o estilo informado.
    Se não encontrar, retorna um dicionário vazio.
    """
    return PRESETS_POR_ESTILO.get(estilo, {})


def estilo_disponivel(estilo: str) -> bool:
    """
    Verifica se o estilo está entre os estilos disponíveis.
    """
    return estilo in PRESETS_POR_ESTILO


def listar_estilos_disponiveis() -> list:
    """
    Retorna todos os estilos disponíveis nos presets.
    """
    return list(PRESETS_POR_ESTILO.keys())


def aplicar_preset_em_config(estilo: str, config_atual: dict) -> dict:
    """
    Mescla os valores do preset ao dicionário de configuração do usuário.
    """
    preset = buscar_preset_por_estilo(estilo)
    nova_config = config_atual.copy()
    nova_config.update(preset)
    return nova_config
