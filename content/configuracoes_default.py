# content/configuracoes_default.py

"""
Presets padrão para estilos de operação do bot Troquinho.

Cada estilo define:
- range_preco: faixa de preço alvo para operar
- indicadores: indicadores técnicos e parâmetros principais
"""

PRESETS_POR_ESTILO = {
    "Day Trade": {
        "range_preco": "1.85–2.15",
        "indicadores": "RSI(14)=45-65, 5 Grids"
    },
    "Scalper": {
        "range_preco": "1.90–2.10",
        "indicadores": "RSI(14)=48-72, 15 Grids"
    },
    "Swing": {
        "range_preco": "1.70–2.30",
        "indicadores": "RSI(14)=40-70, 10 Grids"
    }
}
