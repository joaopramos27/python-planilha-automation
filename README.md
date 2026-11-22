# Automatizador de Planilhas Comerciais

## Sobre o projeto

Pequenos negócios frequentemente perdem horas organizando planilhas de vendas manualmente, corrigindo erros de digitação e montando relatórios do zero. 

Este projeto automatiza todo esse fluxo: a ferramenta importa planilhas de vendas (CSV ou Excel), identifica e separa registros inconsistentes, padroniza os dados, calcula os principais indicadores comerciais e gera um novo relatório em Excel pronto para análise.


## Funcionalidades

- **Importação flexível:** leitura automática de arquivos `.csv` e `.xlsx`.
- **Validação de dados:** detecção de campos obrigatórios vazios, datas inválidas, quantidades ou preços negativos/zerados e registros duplicados, isolando esses erros em uma aba dedicada com o motivo de cada problema.
- **Organização e limpeza:** remoção de espaços extras, padronização de textos, conversão de tipos e ordenação cronológica das vendas.
- **Análise comercial:** cálculo de faturamento total, total de itens vendidos, ticket médio, vendas por categoria e ranking dos produtos mais vendidos.
- **Geração de relatório:** exportação de um arquivo `.xlsx` com múltiplas abas, cabeçalhos estilizados, formatação monetária em Real (`R$`) e ajuste automático da largura das colunas.

## Tecnologias utilizadas

- **Python 3.15.2** — linguagem principal do projeto
- **Pandas** — leitura, limpeza, validação e análise de dados tabulares
- **OpenPyXL** — geração e estilização avançada de planilhas Excel
- **Pytest** — estrutura para testes automatizados
- **Git / GitHub** — controle de versão e hospedagem do código

## Estrutura do projeto

automatizador-planilhas/
├── data/
│   └── vendas_exemplo.csv     # Planilha de entrada para testes
├── output/
│   └── .gitkeep               # Mantém a pasta de saída no repositório
├── src/
│   ├── __init__.py            # Define src como pacote Python
│   ├── main.py                # Orquestra a execução do pipeline
│   ├── validator.py           # Importação e identificação de inconsistências
│   ├── processor.py           # Limpeza, padronização e cálculo por venda
│   ├── analyzer.py            # Indicadores comerciais e rankings
│   └── report.py              # Geração e formatação do relatório Excel
├── tests/                     # Testes automatizados do projeto
├── .gitignore                 # Arquivos ignorados pelo Git
├── README.md                  # Documentação do projeto
└── requirements.txt           # Dependências Python