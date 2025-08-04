from telegram import Update
from telegram.ext import CallbackContext
from services.state_manager import carregar_estado, limpar_estado
from utils.logger import log_interacao


async def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    chat_id = query.message.chat_id
    data = query.data

    await query.answer()

    if data == "ativar_bot":
        config = carregar_estado(chat_id)
        token = config.get("token", "N/A")
        token_resumido = token[:6] + "..." if len(token) > 6 else token

        log_interacao(
            user,
            "✅ Bot ativado pelo usuário",
            etapa="final",
            extra=f"Token configurado: {token_resumido}"
        )

        await query.edit_message_text(
            "🤖 Bot iniciado com sucesso!\nVocê pode monitorar ou pausar a qualquer momento com os comandos disponíveis."
        )

    elif data == "editar_config":
        log_interacao(
            user,
            "🛠 Solicitou edição da configuração",
            etapa="final"
        )

        await query.edit_message_text("🛠 Vamos voltar ao início para editar sua configuração.")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Envie /inicio para recomeçar sua configuração com segurança."
        )

    elif data == "cancelar_config":
        limpar_estado(chat_id)
        log_interacao(
            user,
            "❌ Cancelou a configuração",
            etapa="final"
        )

        await query.edit_message_text(
            "❌ Configuração cancelada. Nenhuma operação foi iniciada."
        )

    else:
        log_interacao(
            user,
            f"❓ Callback desconhecido recebido: {data}",
            etapa="final"
        )

        await query.edit_message_text(
            "❓ Comando não reconhecido. Tente novamente ou envie /ajuda."
        )
