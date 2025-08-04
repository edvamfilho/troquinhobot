import logging
import os
from logging.handlers import RotatingFileHandler

# === Configuração básica do logger principal ===
logger = logging.getLogger("troquinho")
logger.setLevel(logging.INFO)
logger.propagate = False  # evitar duplicação se o root também estiver configurado

# Formatter centralizado: já inclui timestamp, nível e mensagem
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")

# Console handler (já tinha)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    logger.addHandler(console_handler)

# === Adiciona log em arquivo com rotação ===
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
file_path = os.path.join(LOG_DIR, "troquinho.log")
file_handler = RotatingFileHandler(
    file_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
file_handler.setFormatter(formatter)
# só adiciona se não houver um igual (para evitar múltiplas adições em reinícios de import)
if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "") == os.path.abspath(file_path)
           for h in logger.handlers):
    logger.addHandler(file_handler)


# === Helpers de log estruturado ===
def log_interacao(usuario, acao, etapa=None, extra=None):
    # Normaliza dados do usuário para não quebrar se algum campo faltar
    username = getattr(usuario, "username", None) or "sem_username"
    user_id = getattr(usuario, "id", "N/A")
    uid = f"{username} | ID: {user_id}"
    etapa_str = f" | Etapa: {etapa}" if etapa else ""
    extra_str = f" | {extra}" if extra else ""
    logger.info(f"[{uid}] → {acao}{etapa_str}{extra_str}")


def log_erro(usuario, erro, etapa=None):
    username = getattr(usuario, "username", None) or "sem_username"
    user_id = getattr(usuario, "id", "N/A")
    uid = f"{username} | ID: {user_id}"
    etapa_str = f" | Etapa: {etapa}" if etapa else ""
    logger.error(f"[{uid}] ❌ ERRO: {erro}{etapa_str}")
