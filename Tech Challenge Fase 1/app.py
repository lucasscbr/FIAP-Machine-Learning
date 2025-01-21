import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


app = Flask(__name__)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_segura'  # Substitua por uma chave secreta segura
jwt = JWTManager(app)

#Rotas

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validação simplificada (use um banco de dados ou sistema real de autenticação em produção)
    if username == "admin" and password == "senha123":
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    else:
        return jsonify({"msg": "Credenciais inválidas"}), 401

# Rotas para consulta
@app.route('/producao')
@jwt_required()
def get_production_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")
    save_data(tabela, 'producao')
    return (tabela.prettify())

@app.route('/processamentoViniferas')
@jwt_required()
def get_processingwine_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_03")
    save_data(tabela, 'processamento_viniferas')
    return (tabela.prettify())

@app.route('/processamentoAmerican')
@jwt_required()
def get_processingamerican_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_03")
    save_data(tabela, 'processamento_american')
    return (tabela.prettify())

@app.route('/processamentoUvas')
@jwt_required()
def get_processingtablegrapes_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_03")
    save_data(tabela, 'processamento_uvas')
    return (tabela.prettify())

@app.route('/processamentoSemclassificacao')
@jwt_required()
def get_processingwithoutclass_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_03")
    save_data(tabela, 'processamento_sem_classificacao')
    return (tabela.prettify())

@app.route('/comercializacao')
@jwt_required()
def get_commercialization_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04")
    save_data(tabela, 'comercializacao')
    return (tabela.prettify())

@app.route('/importacaoVinhos')
@jwt_required()
def get_wine_import_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_05")
    save_data(tabela, 'importacao_vinhos')
    return (tabela.prettify())

@app.route('/Espumante')
def get_sparklingwine_import_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_05")
    save_data(tabela, 'espumante')
    return (tabela.prettify())

@app.route('/UvasFrescas')
@jwt_required()
def get_freshgrapes_import_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05")
    save_data(tabela, 'uvas_frescas')
    return (tabela.prettify())

@app.route('/UvasPassas')
@jwt_required()
def get_raisins_import_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_05")
    save_data(tabela, 'uvas_passas')
    return (tabela.prettify())

@app.route('/SucoUva')
@jwt_required()
def get_grapejuice_import_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_05")
    save_data(tabela, 'suco_uva')
    return (tabela.prettify())

@app.route('/VinhoExportacao')
@jwt_required()
def get_wine_export_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06")
    save_data(tabela, 'VinhoExportacao')
    return (tabela.prettify())

@app.route('/EspumanteExportacao')
@jwt_required()
def get_sparklingwine_export_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_06")
    save_data(tabela, 'espumante_exportacao')
    return (tabela.prettify())

@app.route('/UvasFrescasExportacao')
@jwt_required()
def get_freshgrapes_export_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_06")
    save_data(tabela, 'uvas_frescas_exportacao')
    return (tabela.prettify())

@app.route('/SucoUvaExportacao')
@jwt_required()
def get_grapejuice_export_data():
    tabela = scrape_embrapa("http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_06")
    save_data(tabela, 'suco_uva_exportacao')
    return (tabela.prettify())


#Métodos
def scrape_embrapa(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_="tb_base tb_dados")
    return table

def save_data(table, nome_arquivo):
    # Converte a tabela para um dataframe pandas e o salva como um csv
    df = pd.read_html(str(table))[0]
    print(df)
    df.to_csv(f'{nome_arquivo}.csv', index=False) 
    

if __name__ == '__main__':
    app.run()



