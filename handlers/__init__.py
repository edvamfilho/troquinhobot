from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

# === Etapa 0: início e jornada ===
from handlers.inicio import inicio_handler, callback_inicio_handler
from handlers.jornada import jornada_handler

# === Etapa 1: onboarding ===
from handlers.etapa_1_onboarding import (
    etapa1_callback_handler,
    resposta_conhecimento_handler,
    resposta_risco_handler
)

# === Etapa 2: menu ===
from handlers.etapa_2_menu.menu import iniciar_etapa2

# === Callback genérico de fallback ===
from handlers.callbacks import callback_handler


def register_handlers(app: Application) -> None:
    # === Comandos principais ===
    app.add_handler(inicio_handler)                             # /inicio
    app.add_handler(CommandHandler("jornada", jornada_handler))  # /jornada

    # === Aliases manuais para retomar etapa 2 ===
    app.add_handler(CommandHandler("etapa2", iniciar_etapa2))
    app.add_handler(CommandHandler("fase2", iniciar_etapa2))

    # === Callbacks inline específicos (ordem importa!) ===
    app.add_handler(callback_inicio_handler)
    app.add_handler(etapa1_callback_handler)           # aceite / recusa termos
    app.add_handler(resposta_conhecimento_handler)
    app.add_handler(resposta_risco_handler)

    # === Callback genérico de fallback: sempre por último ===
    app.add_handler(CallbackQueryHandler(callback_handler))
