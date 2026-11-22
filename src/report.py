from pathlib import Path
import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


def _formatar_aba(ws, colunas_moeda: set[str] | None = None) -> None:
    colunas_moeda = colunas_moeda or set()

    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)

    # Estiliza cabeçalho e mapeia colunas monetárias
    indices_moeda = set()
    for col_idx, cell in enumerate(ws[1], start=1):
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        if str(cell.value).strip().lower() in colunas_moeda:
            indices_moeda.add(col_idx)

    # Formata valores monetários nas linhas de dados
    for row in ws.iter_rows(min_row=2):
        for col_idx, cell in enumerate(row, start=1):
            if col_idx in indices_moeda and isinstance(cell.value, (int, float)):
                cell.number_format = 'R$ #,##0.00'

    # Ajusta largura das colunas automaticamente
    for col in ws.columns:
        max_length = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            valor = "" if cell.value is None else str(cell.value)
            max_length = max(max_length, len(valor))
        ws.column_dimensions[col_letter].width = min(max_length + 4, 45)


def gerar_relatorio_excel(
    analises: dict[str, pd.DataFrame],
    df_processado: pd.DataFrame,
    df_inconsistencias: pd.DataFrame,
    caminho_saida: str | Path,
) -> Path:
    caminho = Path(caminho_saida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    df_export = df_processado.copy()
    if not df_export.empty and "data" in df_export.columns:
        df_export["data"] = df_export["data"].dt.strftime("%d/%m/%Y")

    with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
        analises["resumo"].to_excel(writer, sheet_name="Resumo", index=False)
        analises["produtos_mais_vendidos"].to_excel(
            writer, sheet_name="Top Produtos", index=False
        )
        analises["vendas_por_categoria"].to_excel(
            writer, sheet_name="Categorias", index=False
        )
        df_export.to_excel(writer, sheet_name="Dados Organizados", index=False)

        if not df_inconsistencias.empty:
            df_inconsistencias.to_excel(
                writer, sheet_name="Inconsistencias", index=False
            )

        wb = writer.book
        _formatar_aba(wb["Resumo"])
        _formatar_aba(wb["Top Produtos"], colunas_moeda={"faturamento_total"})
        _formatar_aba(wb["Categorias"], colunas_moeda={"faturamento_total"})
        _formatar_aba(
            wb["Dados Organizados"],
            colunas_moeda={"preco_unitario", "valor_total"},
        )

        if "Inconsistencias" in wb.sheetnames:
            _formatar_aba(wb["Inconsistencias"])

        # Formatação específica das linhas de moeda na aba Resumo
        ws_resumo = wb["Resumo"]
        for row in ws_resumo.iter_rows(min_row=2, max_col=2):
            indicador = str(row[0].value)
            if "(R$)" in indicador and isinstance(row[1].value, (int, float)):
                row[1].number_format = 'R$ #,##0.00'

    return caminho