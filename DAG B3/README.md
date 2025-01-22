# DAG Airflow para Download de Ações do IBOV
Uma DAG AirFlow que usa a api Yahoo Finance para trazer as informações dos últimos cinco pregões de cada ação da B3 (Bolsa de Valores do Brasil) e salva os resultados em arquivos CSV a partir de inputs passados pelos usuários por meio de um arquivo chamado tickers.csv.

## Estrutura do Projeto

### Arquivos

- **tickers.csv**: Um arquivo contendo uma lista de tíckers de ações para coleta de dados. Deve estar localizado no caminho: `/home/airflow/airflowFIAP/codigos/tickers.csv`.
- **01_03_Dag_Acoes_Ibov**: O script principal da DAG para ser incluído no diretório de DAGs do Airflow.

### Exemplo do Arquivo `tickers.csv`

```csv
Ticker
PETR4.SA
VALE3.SA
ITUB4.SA
```
![Figura 2 - Big Data Pipeline - dag acoes ibov](https://github.com/user-attachments/assets/bc76d46a-9c24-433f-863b-1f1884e086e4)

A Task 1 cria o diretório de saída com nome baseado no dia atual (Ano, Mês e Dia), nele ficarão salvas as informações das ações retornadas pela Task 2

## Tecnologias Utilizadas

- **Airflow**: Orquestração de workflows para automação das tarefas.
- **Python**: Linguagem principal para implementação da lógica e processamento de dados.
- **Bibliotecas Python:** 
	- **Pandas**: Manipulação e análise de dados tabulares.
	- **YFinance**: Download de dados financeiros da B3.
	- **Pendulum**: Manipulação de datas e tempos com maior facilidade.
	- **Apache-Airflow**: Comunicação e configuração dos workflows.
- **Linux**: O projeto foi executado em uma máquina virtual ubuntu.
  
## Como Usar

1. **Configurar o Ambiente**:
   - Instale as dependências com `pip install requirements.txt`.
   - Configure o Airflow para incluir o script no diretório de DAGs.

2. **Adicionar o Arquivo de Tickers**:
   - Crie um arquivo `tickers.csv` contendo os tíckers desejados.

3. **Iniciar a DAG**:
   - No Airflow UI, ative a DAG `dag_acoes_ibov`.

4. **Verificar os Resultados**:
   - Os arquivos processados estarão no diretório especificado: `/home/airflow/airflowFIAP/codigos/acoes/YYYYMMDD`.
