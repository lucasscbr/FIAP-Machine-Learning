from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import time
import logging

# Configuração log para saída em um arquivo
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializando o Flask
app = Flask(__name__)

# Carregar o modelo salvo
model = load_model("modelo_lstm_itub4.h5")

# Configurando o MinMaxScaler para normalizar
scaler = MinMaxScaler(feature_range=(0, 1))

# Inicia o timer quando recebe requisições
@app.before_request
def start_timer():
    request.start_time = time.time()

# Finaliza o timer quando a requisição termina
@app.after_request
def log_request(response):
    elapsed_time = time.time() - request.start_time
    print(f"Requisição para {request.path} levou {elapsed_time:.2f}s")
    logging.info(f"Requisicao para {request.path} levou {elapsed_time:.2f}s")
    return response

# Endpoint para prever preços
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receber dados do usuário (JSON)
        data = request.json
        prices = data['prices']  # Lista de preços históricos fornecida pelo usuário
        days_to_predict = data['days']  # Número de dias a prever
        
        # Validação
        if not isinstance(days_to_predict, int):
            return jsonify({"error": "Forneça o número de dias a prever."})
        
        if len(prices) < 60:
            return jsonify({"error": "Dados insuficientes! São necessários pelo menos 61 preços históricos."})
        
        # Converter os dados em um DataFrame
        df = pd.DataFrame(prices, columns=["Close"])
        
        # Normalizar os dados
        scaled_data = scaler.fit_transform(df)
        
        # Criar a sequência inicial
        sequence_length = 60
        input_sequence = scaled_data[-sequence_length:]  # Pega os últimos 60 preços normalizados
        predictions = []
        
        # Iterar para gerar múltiplas previsões
        for _ in range(days_to_predict):
            # Ajustar a dimensão para o modelo
            last_sequence = np.array([input_sequence])
            
            # Fazer a previsão
            predicted_scaled = model.predict(last_sequence)
            
            # Desnormalizar o valor previsto
            predicted_price = scaler.inverse_transform(predicted_scaled)
            predictions.append(predicted_price[0][0])
            
            # Atualizar a sequência de entrada
            next_input = np.append(input_sequence[1:], predicted_scaled, axis=0)
            input_sequence = next_input
        
        # Retornar as previsões como JSON
        print('predictions',predictions)
        predictions = [float(value) for value in predictions]
        return jsonify({"predicted_prices": predictions})
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Rodar o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
