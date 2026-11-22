import pandas as pd


def processar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df_limpo = df.copy()

    # Limpeza e padronização de texto
    colunas_texto = ["produto", "categoria"]
    if "vendedor" in df_limpo.columns:
        colunas_texto.append("vendedor")

    for col in colunas_texto:
        df_limpo[col] = (
            df_limpo[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )

    # Conversão de tipos
    df_limpo["data"] = pd.to_datetime(df_limpo["data"])
    df_limpo["quantidade"] = pd.to_numeric(df_limpo["quantidade"]).astype(int)
    df_limpo["preco_unitario"] = pd.to_numeric(df_limpo["preco_unitario"]).round(2)

    # Cálculo do total da venda por linha
    df_limpo["valor_total"] = (
        df_limpo["quantidade"] * df_limpo["preco_unitario"]
    ).round(2)

    # Organização cronológica
    df_limpo = df_limpo.sort_values(by="data", ascending=True).reset_index(drop=True)

    return df_limpo