from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from services.state_manager import obter_estado_usuario, carregar_estado
from handlers.etapa_1_onboarding.termos import iniciar_etapa1
from handlers.etapa_2_menu.menu import iniciar_etapa2
from utils.resumooperacao import gerar_resumo_config
from utils.logger import log_interacao


async def comando_jornada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    estado = obter_estado_usuario(chat_id)
    etapa = estado.get("etapa", "etapa1")

    log_interacao(
        user, f"Retomando jornada – etapa atual: {etapa}", etapa=etapa)

    try:
        if etapa == "etapa1":
            await context.bot.send_message(
                chat_id=chat_id,
                text="🚀 Vamos começar sua trilha de conhecimento!"
            )
            await iniciar_etapa1(update, context)

        elif etapa == "etapa2":
            await context.bot.send_message(
                chat_id=chat_id,
                text="🔄 Retomando sua jornada na etapa 2"
            )
            await iniciar_etapa2(update, context)

        # Etapa 3 deixada em standby para desenvolvimento futuro
        # elif etapa == "etapa3":
        #     await context.bot.send_message(
        #         chat_id=chat_id,
        #         text="⚙️ Etapa 3 em construção..."
        #     )
        #     await iniciar_etapa3(update, context)

        elif etapa == "final":
            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ Você já concluiu todas as etapas! Use /configurar para ajustar seu bot."
            )
            log_interacao(user, "Usuário já finalizou a jornada", etapa=etapa)

        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Algo deu errado. Use /inicio para recomeçar."
            )
            log_interacao(
                user, f"Estado inválido detectado: {etapa}", etapa="erro")

    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Ocorreu um erro ao retomar sua jornada. Tente novamente com /jornada ou /inicio."
        )
        log_interacao(user, "Erro ao executar etapa da jornada",
                      etapa=etapa, extra=str(e))


async def finalizar_etapas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    user_config = carregar_estado(chat_id)
    resumo_texto, botoes = gerar_resumo_config(user_config)

    await context.bot.send_message(
        chat_id=chat_id,
        text=resumo_texto,
        parse_mode='HTML',
        reply_markup=botoes
    )
    log_interacao(user, "Enviou resumo final da jornada", etapa="final")


jornada_handler = CommandHandler("jornada", comando_jornada)
