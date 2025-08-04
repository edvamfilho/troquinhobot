# handlers/etapa_1_onboarding/quiz_conhecimento.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler
from content.mensagens import MENSAGEM_CONHECIMENTO_FINAL
from services.state_manager import salvar_resposta_conhecimento, inferir_nivel_conhecimento, carregar_estado
from utils.logger import log_interacao
from handlers.etapa_1_onboarding.perfil_risco import enviar_proxima_pergunta_risco
from handlers.perguntas import PERGUNTAS_CONHECIMENTO



async def perguntar_conhecimento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    usuario = context.user_data.get("usuario", {})
    idx = usuario.get("indice_conhecimento", 0)

    if idx >= len(PERGUNTAS_CONHECIMENTO):
        estado = carregar_estado(user_id)
        respostas = estado.get("respostas_conhecimento", {})
        nivel = inferir_nivel_conhecimento(respostas) or "Indefinido"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MENSAGEM_CONHECIMENTO_FINAL.format(nivel=nivel)
        )
        await enviar_proxima_pergunta_risco(update, context)
        return

    pergunta = PERGUNTAS_CONHECIMENTO[idx]
    keyboard = [[InlineKeyboardButton(
        text=resp, callback_data=f"resposta_conhecimento|{idx}|{resp}")] for resp in pergunta["respostas"]]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📘 Pergunta {idx + 1}/{len(PERGUNTAS_CONHECIMENTO)}\n\n{pergunta['pergunta']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    log_interacao(update, etapa="etapa1",
                  acao=f"Enviou pergunta de conhecimento #{idx + 1}: {pergunta['pergunta']}")


async def resposta_conhecimento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data.split("|")

    idx = int(data[1])
    resposta = data[2]

    salvar_resposta_conhecimento(user_id, idx, resposta)

    context.user_data.setdefault("usuario", {})[
        "indice_conhecimento"] = idx + 1

    log_interacao(update, etapa="etapa1",
                  acao=f"Respondeu conhecimento #{idx + 1}: {resposta}")
    await perguntar_conhecimento(update, context)

# ✅ Handler com escape correto
resposta_conhecimento_handler = CallbackQueryHandler(
    resposta_conhecimento, pattern=r"^resposta_conhecimento\|"
)
