# pip install selenium pandas pyarrow

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

navegador = webdriver.Chrome()

navegador.get("https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br")

select_consulta = Select(navegador.find_element(By.XPATH,'//*[@id="segment"]'))
select_consulta.select_by_visible_text('Setor de Atuação')

# Aguarda até que o elemento da página esteja visível
elemento_pagina = WebDriverWait(navegador, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="selectPage"]'))
)

# Seleciona "120" no resultados por página
select_pagina = Select(navegador.find_element(By.XPATH, '//*[@id="selectPage"]'))
select_pagina.select_by_visible_text('120')

# Encontra a tabela no HTML
table = navegador.find_element(By.CLASS_NAME, 'table-responsive-md')

# Extrai os dados da tabela
data = []
headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]

for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:
    cells = row.find_elements(By.TAG_NAME, 'td')
    if len(cells) > 1:
        data.append([cell.text.strip() for cell in cells])

# Fecha o driver
navegador.quit()

# Verifica se o número de colunas é consistente
max_columns = len(headers)
for row in data:
    while len(row) < max_columns:
        row.append('')  # Adiciona células vazias conforme necessário

# Cria um DataFrame com os dados
df = pd.DataFrame(data, columns=headers)

# Salva os dados em formato Parquet
df.to_parquet('dadosTabela.parquet', engine='pyarrow')

# Salva os dados em formato CSV
df.to_csv('dadosTabela.csv', index=False)

print("Dados salvos com sucesso em dadosTabela.parquet e dadosTabela.csv")