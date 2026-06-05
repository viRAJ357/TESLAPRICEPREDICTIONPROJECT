import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Title
cells.append(nbf.v4.new_markdown_cell("# Tesla Stock Price Prediction\n\nThis notebook contains the complete pipeline for Data Preprocessing, Deep Learning Modeling (SimpleRNN and LSTM), Evaluation, and Hyperparameter Tuning for predicting Tesla stock prices."))

# Imports
code_imports = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, SimpleRNN, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import warnings
warnings.filterwarnings('ignore')

print(tf.__version__)"""
cells.append(nbf.v4.new_code_cell(code_imports))

# Load data
code_load = """# 1. Data Preprocessing & Cleaning
# Load the dataset
df = pd.read_csv('TSLA.csv')
display(df.head())

# Check for missing values
print("Missing values in dataset:")
print(df.isnull().sum())

# If there were missing values, we could use forward fill: df.fillna(method='ffill', inplace=True)"""
cells.append(nbf.v4.new_code_cell(code_load))

# Feature Selection and Datetime
code_datetime = """# Convert Date to datetime and set as index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# We will focus on the 'Adj Close' price for this project
data = df[['Adj Close']]
display(data.head())"""
cells.append(nbf.v4.new_code_cell(code_datetime))

# Visualization
code_vis = """# Data Visualization
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Adj Close'], label='Tesla Adj Close Price')
plt.title('Tesla Stock Price History')
plt.xlabel('Date')
plt.ylabel('Adj Close Price USD')
plt.legend()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code_vis))

# Scaling
code_scaling = """# 2. Scaling the Data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

print(f"Shape of scaled data: {scaled_data.shape}")"""
cells.append(nbf.v4.new_code_cell(code_scaling))

# Sequence Generation
code_seq = """# Prepare sequences for LSTM/SimpleRNN
def create_sequences(dataset, time_step=60):
    X, Y = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        X.append(a)
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)

time_step = 60
X, y = create_sequences(scaled_data, time_step)

# Reshape input to be [samples, time steps, features]
X = X.reshape(X.shape[0], X.shape[1], 1)

print(f"Shape of X: {X.shape}")
print(f"Shape of y: {y.shape}")

# Train-Test Split (80% training, 20% testing)
train_size = int(len(X) * 0.8)
test_size = len(X) - train_size

X_train, X_test = X[0:train_size], X[train_size:len(X)]
y_train, y_test = y[0:train_size], y[train_size:len(y)]

print(f"Training data shape: {X_train.shape}")
print(f"Testing data shape: {X_test.shape}")"""
cells.append(nbf.v4.new_code_cell(code_seq))

# Model Definition - SimpleRNN
code_rnn = """# 3. Model Development

# 3.1 Define SimpleRNN Architecture
def build_simplernn(units=50, dropout_rate=0.2, learning_rate=0.001):
    model = Sequential()
    model.add(SimpleRNN(units=units, return_sequences=True, input_shape=(time_step, 1)))
    model.add(Dropout(dropout_rate))
    model.add(SimpleRNN(units=units))
    model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

rnn_model = build_simplernn()
rnn_model.summary()"""
cells.append(nbf.v4.new_code_cell(code_rnn))

# Model Definition - LSTM
code_lstm = """# 3.1 Define LSTM Architecture
def build_lstm(units=50, dropout_rate=0.2, learning_rate=0.001):
    model = Sequential()
    model.add(LSTM(units=units, return_sequences=True, input_shape=(time_step, 1)))
    model.add(Dropout(dropout_rate))
    model.add(LSTM(units=units))
    model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

lstm_model = build_lstm()
lstm_model.summary()"""
cells.append(nbf.v4.new_code_cell(code_lstm))

# Training Models
code_train = """# 3.3 Model Training
# Define callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

print("Training SimpleRNN...")
history_rnn = rnn_model.fit(X_train, y_train, validation_data=(X_test, y_test), 
                            epochs=50, batch_size=32, callbacks=[early_stop], verbose=1)

print("\\nTraining LSTM...")
history_lstm = lstm_model.fit(X_train, y_train, validation_data=(X_test, y_test), 
                              epochs=50, batch_size=32, callbacks=[early_stop], verbose=1)"""
cells.append(nbf.v4.new_code_cell(code_train))

# Evaluate Models
code_eval = """# 4. Model Evaluation & Prediction
# Predictions
train_predict_rnn = rnn_model.predict(X_train)
test_predict_rnn = rnn_model.predict(X_test)

train_predict_lstm = lstm_model.predict(X_train)
test_predict_lstm = lstm_model.predict(X_test)

# Inverse transform to get actual prices
train_predict_rnn = scaler.inverse_transform(train_predict_rnn)
test_predict_rnn = scaler.inverse_transform(test_predict_rnn)
train_predict_lstm = scaler.inverse_transform(train_predict_lstm)
test_predict_lstm = scaler.inverse_transform(test_predict_lstm)

actual_y_train = scaler.inverse_transform(y_train.reshape(-1, 1))
actual_y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

# Calculate RMSE (Root Mean Squared Error) and MSE
mse_rnn = mean_squared_error(actual_y_test, test_predict_rnn)
mse_lstm = mean_squared_error(actual_y_test, test_predict_lstm)

print(f"SimpleRNN Test MSE: {mse_rnn:.4f}")
print(f"LSTM Test MSE: {mse_lstm:.4f}")"""
cells.append(nbf.v4.new_code_cell(code_eval))

# Plot Predictions
code_plot = """# Plotting Actual vs Predicted for LSTM
plt.figure(figsize=(14, 7))
plt.plot(data.index[len(data) - len(actual_y_test):], actual_y_test, color='blue', label='Actual Tesla Stock Price')
plt.plot(data.index[len(data) - len(test_predict_rnn):], test_predict_rnn, color='red', label='SimpleRNN Predicted Price')
plt.plot(data.index[len(data) - len(test_predict_lstm):], test_predict_lstm, color='green', label='LSTM Predicted Price')
plt.title('Tesla Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Adj Close Price USD')
plt.legend()
plt.show()"""
cells.append(nbf.v4.new_code_cell(code_plot))

# GridSearchCV setup
code_grid = """# Hyperparameter Tuning using GridSearchCV (Conceptual Demonstration / Manual Loop)
# Note: KerasClassifier/KerasRegressor from SciKeras is usually used, but we'll do a simple parameter search to avoid dependency issues

units_options = [50, 100]
dropout_options = [0.2]
learning_rate_options = [0.001]

best_score = float('inf')
best_params = {}

print("Starting manual GridSearch for LSTM...")
for units in units_options:
    for dropout in dropout_options:
        for lr in learning_rate_options:
            print(f"Testing units={units}, dropout={dropout}, lr={lr}")
            model = build_lstm(units=units, dropout_rate=dropout, learning_rate=lr)
            # Use a smaller subset for faster tuning
            model.fit(X_train[:500], y_train[:500], epochs=10, batch_size=32, verbose=0)
            preds = model.predict(X_test)
            preds_inv = scaler.inverse_transform(preds)
            mse = mean_squared_error(actual_y_test, preds_inv)
            if mse < best_score:
                best_score = mse
                best_params = {'units': units, 'dropout_rate': dropout, 'learning_rate': lr}

print(f"Best parameters found: {best_params} with MSE: {best_score}")"""
cells.append(nbf.v4.new_code_cell(code_grid))

# Future Predictions
code_future = """# Predict 1 day, 5 days, and 10 days into the future
def predict_future(model, last_sequence, days=1):
    future_preds = []
    curr_seq = last_sequence.copy()
    
    for _ in range(days):
        pred = model.predict(curr_seq.reshape(1, time_step, 1), verbose=0)
        future_preds.append(pred[0,0])
        # Append prediction and remove the first element to keep sequence length constant
        curr_seq = np.append(curr_seq[1:], pred)
        
    return scaler.inverse_transform(np.array(future_preds).reshape(-1, 1))

last_seq = scaled_data[-time_step:]

print("--- SimpleRNN Predictions ---")
print("1 Day Future:", predict_future(rnn_model, last_seq, days=1)[0][0])
print("5 Days Future:\\n", predict_future(rnn_model, last_seq, days=5).flatten())
print("10 Days Future:\\n", predict_future(rnn_model, last_seq, days=10).flatten())

print("\\n--- LSTM Predictions ---")
print("1 Day Future:", predict_future(lstm_model, last_seq, days=1)[0][0])
print("5 Days Future:\\n", predict_future(lstm_model, last_seq, days=5).flatten())
print("10 Days Future:\\n", predict_future(lstm_model, last_seq, days=10).flatten())"""
cells.append(nbf.v4.new_code_cell(code_future))

nb['cells'] = cells
with open('Tesla_Stock_Prediction.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Jupyter Notebook 'Tesla_Stock_Prediction.ipynb' created successfully.")
