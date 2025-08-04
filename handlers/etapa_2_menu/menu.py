from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.logger import log_interacao
from services.state_manager import atualizar_estado


async def iniciar_etapa2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    botoes = [
        [InlineKeyboardButton("📚 Aprender sobre Web3", callback_data="menu_aprender")],
        [InlineKeyboardButton("💼 Abrir carteira", callback_data="menu_abrir_carteira")],
        [InlineKeyboardButton("📊 Analisar mercado", callback_data="menu_analisar")],
        [InlineKeyboardButton("🔌 Conectar carteira", callback_data="menu_conectar")],
        [InlineKeyboardButton("🧪 Testar estratégias", callback_data="menu_testar")],
        [InlineKeyboardButton("🤖 Iniciar Bot trader", callback_data="menu_bot_trader")],
    ]

    await context.bot.send_message(
        chat_id=chat_id,
        text="🔍 O que você deseja fazer agora?",
        reply_markup=InlineKeyboardMarkup(botoes)
    )

    atualizar_estado(chat_id, {"etapa": "etapa2"})
    log_interacao(user, "Entrou no menu principal (etapa 2)", etapa="etapa2")
