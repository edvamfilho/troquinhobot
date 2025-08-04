import logging
from config.settings import TELEGRAM_TOKEN
from handlers import register_handlers

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# === FUNÇÕES DE COMANDO BÁSICAS ===


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Eu sou o Troquinho, seu bot educativo cripto. Use /inicio para começar ou /ajuda para mais opções."
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Comandos disponíveis:\n"
        "/inicio – Começar do zero\n"
        "/jornada – Continuar de onde parou\n"
        "/ajuda – Ver instruções"
    )

# === LOGGING E INICIALIZAÇÃO DO APP ===

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Handlers principais
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ajuda", ajuda))

# Handlers internos do bot
register_handlers(app)

print("🤖 Bot Troquinho rodando...")
app.run_polling()
