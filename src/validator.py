from pathlib import Path
import pandas as pd

COLUNAS_OBRIGATORIAS = {
    "data",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
}


def carregar_arquivo(caminho_arquivo: str | Path) -> pd.DataFrame:
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    extensao = caminho.suffix.lower()
    if extensao == ".csv":
        df = pd.read_csv(caminho)
    elif extensao in {".xlsx", ".xls"}:
        df = pd.read_excel(caminho)
    else:
        raise ValueError(f"Formato não suportado: {extensao}. Use .csv ou .xlsx.")

    # Padroniza nomes de colunas para minúsculas e sem espaços extras
    df.columns = [str(col).strip().lower() for col in df.columns]

    colunas_faltantes = COLUNAS_OBRIGATORIAS - set(df.columns)
    if colunas_faltantes:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {', '.join(sorted(colunas_faltantes))}"
        )

    return df


def validar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_trabalho = df.copy()
    erros = pd.Series("", index=df_trabalho.index, dtype="object")

    def registrar_erro(mascara: pd.Series, mensagem: str) -> None:
        nonlocal erros
        erros = erros.where(~mascara, erros + f"{mensagem}; ")

    # 1. Campos obrigatórios nulos ou vazios
    produto_vazio = df_trabalho["produto"].isna() | (
        df_trabalho["produto"].astype(str).str.strip() == ""
    )
    registrar_erro(produto_vazio, "Produto ausente")

    categoria_vazia = df_trabalho["categoria"].isna() | (
        df_trabalho["categoria"].astype(str).str.strip() == ""
    )
    registrar_erro(categoria_vazia, "Categoria ausente")

    # 2. Validação de data
    datas_convertidas = pd.to_datetime(df_trabalho["data"], errors="coerce")
    registrar_erro(datas_convertidas.isna(), "Data inválida")

    # 3. Validação numérica de quantidade e preço unitário
    qtd_numerica = pd.to_numeric(df_trabalho["quantidade"], errors="coerce")
    registrar_erro(qtd_numerica.isna() | (qtd_numerica <= 0), "Quantidade inválida (<= 0 ou não numérica)")

    preco_numerico = pd.to_numeric(df_trabalho["preco_unitario"], errors="coerce")
    registrar_erro(preco_numerico.isna() | (preco_numerico <= 0), "Preço unitário inválido (<= 0 ou não numérico)")

    # 4. Linhas duplicadas exatas
    duplicadas = df_trabalho.duplicated(keep="first")
    registrar_erro(duplicadas, "Registro duplicado")

    tem_erro = erros != ""

    df_inconsistencias = df_trabalho[tem_erro].copy()
    df_inconsistencias["motivo_erro"] = erros[tem_erro].str.rstrip("; ")

    df_valido = df_trabalho[~tem_erro].copy()

    return df_valido, df_inconsistencias