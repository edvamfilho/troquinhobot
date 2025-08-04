from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def formatar_valor(valor, sufixo=""):
    """
    Formata números com duas casas decimais ou retorna 'Não informado'.
    """
    try:
        return f"{float(valor):,.2f}{sufixo}"
    except (ValueError, TypeError):
        return "Não informado"


def formatar_lista_ou_dict(valor):
    """
    Formata listas ou dicionários para string legível, ou retorna string padrão.
    """
    if isinstance(valor, dict):
        return ', '.join(f"{k}: {v}" for k, v in valor.items())
    elif isinstance(valor, list):
        return ', '.join(str(v) for v in valor)
    elif isinstance(valor, str):
        return valor
    return "Padrão"


def gerar_resumo_config(user_config):
    risco = user_config.get('perfil_risco', 'Não definido')
    estilo = user_config.get('estilo_operacao', 'Não definido')
    token = user_config.get('token', 'Não definido')
    capital = formatar_valor(user_config.get('capital_total'), " USDT")
    por_trade = formatar_valor(user_config.get('valor_por_trade'), " USDT")
    engine = user_config.get('estrategia', 'Grid')
    indicadores = formatar_lista_ou_dict(user_config.get('indicadores'))
    grids = formatar_lista_ou_dict(user_config.get('grids'))

    texto = (
        "🎛️ <b>Resumo da Configuração</b>\n"
        f"• <b>Risco:</b> {risco}\n"
        f"• <b>Estilo:</b> {estilo}\n"
        f"• <b>Engine:</b> {engine}\n"
        f"• <b>Token:</b> {token}\n"
        f"• <b>Capital:</b> {capital} ({por_trade} por trade)\n"
        f"• <b>Indicadores:</b> {indicadores}\n"
        f"• <b>Grids:</b> {grids}\n"
    )

    botoes = [
        [InlineKeyboardButton("✅ Iniciar Bot", callback_data="ativar_bot")],
        [InlineKeyboardButton("🔁 Editar", callback_data="editar_config")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_config")]
    ]

    return texto, InlineKeyboardMarkup(botoes)
