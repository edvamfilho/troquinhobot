# handlers/etapa_1_onboarding/termos.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from services.state_manager import atualizar_estado
from content.mensagens import TERMOS_DE_USO
from .apresentacao import mostrar_apresentacao


async def iniciar_etapa1(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("✅ Aceito", callback_data="aceitar_termos")],
        [InlineKeyboardButton("❌ Recusar", callback_data="recusar_termos")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(TERMOS_DE_USO, reply_markup=reply_markup)


async def etapa1_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "aceitar_termos":
        await query.answer("Você aceitou os termos!")
        atualizar_estado(user_id, {"etapa": "etapa1"})
        await mostrar_apresentacao(update, context)

    elif query.data == "recusar_termos":
        await query.answer("Você recusou os termos.")
        await query.message.reply_text("Para usar o bot, é necessário aceitar os termos.")

etapa1_callback_handler = CallbackQueryHandler(
    etapa1_callback, pattern="^(aceitar_termos|recusar_termos)$")
