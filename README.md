### 📌 Prioridade 1 – Arquivos iniciais:

| Ordem | Arquivo                                   | Papel                                                                       |
| ----- | ----------------------------------------- | --------------------------------------------------------------------------- |
| 1     | `bot.py`                                | Inicia a aplicação e chama `register_handlers`                          |
| 2     | `handlers/__init__.py`                  | Registra os handlers de forma centralizada                                  |
| 3     | `handlers/inicio.py`                    | Comando `/inicio`e botão “iniciar trilha”                              |
| 4     | `handlers/jornada.py`                   | Lida com a transição para `etapa_1_onboarding`                          |
| 5     | `handlers/etapa_1_onboarding/termos.py` | Exibe termos e processa aceitação                                         |
| 6     | `content/mensagens.py`                  | Armazena os textos de interface, como termos, mensagens de boas-vindas etc. |
