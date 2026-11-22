from pathlib import Path
from src.validator import carregar_arquivo, validar_dados
from src.processor import processar_dados
from src.analyzer import analisar_vendas
from src.report import gerar_relatorio_excel


def executar_pipeline(arquivo_entrada: Path, arquivo_saida: Path) -> None:
    print(f"Lendo arquivo: {arquivo_entrada}")
    df_bruto = carregar_arquivo(arquivo_entrada)

    df_valido, df_inconsistencias = validar_dados(df_bruto)
    print(f"Registros válidos: {len(df_valido)}")
    print(f"Registros inconsistentes encontrados: {len(df_inconsistencias)}")

    df_processado = processar_dados(df_valido)
    analises = analisar_vendas(df_processado)

    caminho_final = gerar_relatorio_excel(
        analises=analises,
        df_processado=df_processado,
        df_inconsistencias=df_inconsistencias,
        caminho_saida=arquivo_saida,
    )

    print(f"\nRelatório gerado com sucesso em: {caminho_final}")


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent
    entrada = raiz / "data" / "vendas_exemplo.csv"
    saida = raiz / "output" / "relatorio_vendas.xlsx"

    executar_pipeline(entrada, saida)