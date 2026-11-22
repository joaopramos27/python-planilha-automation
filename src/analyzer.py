import pandas as pd


def analisar_vendas(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    if df.empty:
        return {
            "resumo": pd.DataFrame(columns=["Indicador", "Valor"]),
            "produtos_mais_vendidos": pd.DataFrame(),
            "vendas_por_categoria": pd.DataFrame(),
        }

    faturamento_total = df["valor_total"].sum()
    total_itens = int(df["quantidade"].sum())
    total_pedidos = len(df)
    ticket_medio = faturamento_total / total_pedidos if total_pedidos > 0 else 0.0
    periodo = f"{df['data'].min().strftime('%d/%m/%Y')} a {df['data'].max().strftime('%d/%m/%Y')}"

    resumo = pd.DataFrame(
        {
            "Indicador": [
                "Período Analisado",
                "Total de Vendas (Pedidos)",
                "Total de Itens Vendidos",
                "Faturamento Total (R$)",
                "Ticket Médio (R$)",
            ],
            "Valor": [
                periodo,
                total_pedidos,
                total_itens,
                round(faturamento_total, 2),
                round(ticket_medio, 2),
            ],
        }
    )

    produtos_mais_vendidos = (
        df.groupby("produto", as_index=False)
        .agg(
            quantidade_vendida=("quantidade", "sum"),
            faturamento_total=("valor_total", "sum"),
            pedidos=("produto", "count"),
        )
        .sort_values(by=["quantidade_vendida", "faturamento_total"], ascending=False)
        .reset_index(drop=True)
    )

    vendas_por_categoria = (
        df.groupby("categoria", as_index=False)
        .agg(
            quantidade_vendida=("quantidade", "sum"),
            faturamento_total=("valor_total", "sum"),
        )
        .sort_values(by="faturamento_total", ascending=False)
        .reset_index(drop=True)
    )

    return {
        "resumo": resumo,
        "produtos_mais_vendidos": produtos_mais_vendidos,
        "vendas_por_categoria": vendas_por_categoria,
    }