from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

from content.mensagens import MENSAGEM_INICIAL as mensagem_inicio, TERMOS_DE_USO as texto_termos
from services.state_manager import criar_usuario
from utils.logger import log_interacao


# === Comando /inicio ===
async def comando_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    criar_usuario(chat_id)
    log_interacao(user, "Usuário iniciou com /inicio", etapa="inicio")

    botoes = [
        [InlineKeyboardButton("▶️ Começar", callback_data="iniciar_trilha")],
        [InlineKeyboardButton("📄 Ver Termos", callback_data="ver_termos")]
    ]

    await context.bot.send_message(
        chat_id=chat_id,
        text=mensagem_inicio,
        reply_markup=InlineKeyboardMarkup(botoes),
        parse_mode="Markdown"
    )


# === Callback dos botões ===
async def callback_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    chat_id = query.message.chat.id
    data = query.data

    log_interacao(user, f"Clicou em botão: {data}", etapa="inicio")

    if data == "ver_termos":
        await context.bot.send_message(
            chat_id=chat_id,
            text=texto_termos,
            parse_mode="Markdown"
        )

    elif data == "iniciar_trilha":
        try:
            from handlers.etapa_1_onboarding.termos import iniciar_etapa1
            await iniciar_etapa1(update, context)
        except Exception as e:
            log_interacao(user, "❌ Erro ao iniciar trilha",
                          etapa="inicio", extra=str(e))
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Ocorreu um erro ao iniciar sua trilha. Tente novamente mais tarde."
            )

    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="❓ Opção não reconhecida. Tente novamente."
        )
        log_interacao(user, f"❓ Callback desconhecido: {data}", etapa="inicio")


inicio_handler = CommandHandler("inicio", comando_inicio)
callback_inicio_handler = CallbackQueryHandler(
    callback_inicio, pattern="^(ver_termos|iniciar_trilha)$"
)
