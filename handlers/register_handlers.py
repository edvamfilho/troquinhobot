from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from handlers.inicio import inicio_handler, callback_inicio_handler
from handlers.jornada import jornada_handler

from handlers.etapa_1_onboarding.termos import etapa1_callback_handler
from handlers.etapa_1_onboarding.quiz_conhecimento import resposta_conhecimento_handler
from handlers.etapa_1_onboarding.perfil_risco import resposta_risco_handler

from handlers.etapa_2_menu.menu import iniciar_etapa2  # Corrigido nome da etapa
from handlers.callbacks import callback_handler  # fallback genérico


def register_handlers(app: Application) -> None:
    # === Comandos principais ===
    app.add_handler(inicio_handler)
    app.add_handler(CommandHandler("jornada", jornada_handler))

    # === Comandos manuais para pular etapas
    app.add_handler(CommandHandler("etapa2", iniciar_etapa2))
    app.add_handler(CommandHandler("fase2", iniciar_etapa2))

    # === Callbacks específicos da etapa 1
    app.add_handler(callback_inicio_handler)
    app.add_handler(etapa1_callback_handler)
    app.add_handler(resposta_conhecimento_handler)
    app.add_handler(resposta_risco_handler)

    # === Fallback genérico
    app.add_handler(CallbackQueryHandler(callback_handler))
