from telegram import Update
from telegram.ext import ContextTypes

from utils.logger import log_interacao
from handlers.etapa_1_onboarding.quiz_conhecimento import perguntar_conhecimento


async def mostrar_apresentacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensagem de boas-vindas e introdução à jornada."""
    chat_id = update.effective_chat.id
    user = update.effective_user

    mensagem = (
        "🎓 Bem-vindo à Jornada Troquinho!\n\n"
        "Vamos entender o quanto você já sabe sobre criptomoedas e seu perfil de risco.\n"
        "Responda algumas perguntas rápidas e siga aprendendo com a gente. 🚀"
    )

    await context.bot.send_message(chat_id=chat_id, text=mensagem)
    log_interacao(user, "Enviada introdução da jornada", etapa="etapa1")

    # Avança para o quiz
    await perguntar_conhecimento(update, context)
