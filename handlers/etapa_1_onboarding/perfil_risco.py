from telegram.ext import CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler
from content.mensagens import MENSAGEM_FINAL_RISCO
from services.state_manager import salvar_resposta_risco, inferir_perfil_risco
from utils.logger import log_interacao
from handlers.perguntas import PERGUNTAS_RISCO


async def enviar_proxima_pergunta_risco(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    usuario = context.user_data.get("usuario", {})
    idx = usuario.get("indice_risco", 0)

    if idx >= len(PERGUNTAS_RISCO):
        perfil = inferir_perfil_risco(user_id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=MENSAGEM_FINAL_RISCO.format(perfil=perfil))
        log_interacao(update, etapa="etapa1",
                      acao=f"Perfil de risco inferido: {perfil}")
        return

    pergunta = PERGUNTAS_RISCO[idx]
    keyboard = [[InlineKeyboardButton(
        text=resp, callback_data=f"resposta_risco|{idx}|{resp}")] for resp in pergunta["respostas"]]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"⚠️ Pergunta {idx + 1}/{len(PERGUNTAS_RISCO)}\n\n{pergunta['pergunta']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    log_interacao(update, etapa="etapa1",
                  acao=f"Enviou pergunta de risco #{idx + 1}: {pergunta['pergunta']}")


async def resposta_risco(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data.split("|")

    idx = int(data[1])
    resposta = data[2]

    salvar_resposta_risco(user_id, idx, resposta)
    context.user_data.setdefault("usuario", {})["indice_risco"] = idx + 1

    log_interacao(update, etapa="etapa1",
                  acao=f"Respondeu risco #{idx + 1}: {resposta}")
    await enviar_proxima_pergunta_risco(update, context)

# ✅ Handler com raw string para evitar warnings
resposta_risco_handler = CallbackQueryHandler(
    resposta_risco, pattern=r"^resposta_risco\|"
)
