import numpy as np
import pandas as pd
import tensorflow as tf
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.layers import Dropout

# Configuração que gerou o modelo com 70,22% de RMSE
# Coletando ações do Itaú
symbol = 'ITUB4.SA'
start_date = '2019-01-01'
end_date = '2024-07-1'
df = yf.download(symbol, start=start_date, end=end_date)
df = df[['Close']]
df.head()

# Normalizando os dados
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df)

# Função para criar sequências de entrada e saída
def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    return np.array(X), np.array(y)

# Configuração das sequências
sequence_length = 60  # Usando 60 dias anteriores para prever o próximo dia
X, y = create_sequences(scaled_data, sequence_length)

# Dividindo entre treino (70%) e teste (30%)
train_size = int(len(X) * 0.7)
train_X, test_X = X[:train_size], X[train_size:]
train_y, test_y = y[:train_size], y[train_size:]

# Modelo LSTM
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2])),
    Dropout(0.2),
    LSTM(50, return_sequences=True),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25),
    Dense(1)
])

# Compilando o modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Treinando o modelo
history = model.fit(train_X, train_y, validation_data=(test_X, test_y),
                    epochs=100, batch_size=32, verbose=1) 

# Avaliando o modelo
predictions = model.predict(test_X)
predictions = scaler.inverse_transform(predictions)  # Desnormalizando as previsões
real_values = scaler.inverse_transform(test_y)

# Calculando RMSE
rmse = np.sqrt(mean_squared_error(real_values, predictions))
print("Root Mean Squared Error (RMSE):", rmse)

# Salvando o modelo completo em um único arquivo
model.save("modelo_lstm_itub4.h5")
print("Modelo salvo como 'modelo_lstm_itub4.h5'")
