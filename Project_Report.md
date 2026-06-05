# Tesla Stock Price Prediction: Project Report

## 1. Introduction and Problem Statement
The objective of this project is to develop a deep learning-based predictive model to forecast the future stock price of Tesla based on historical closing prices. Stock price data is intrinsically sequential, meaning that past values have a significant impact on future trends. Standard machine learning models often struggle to capture these temporal dependencies, which is why we turned to deep learning approaches designed for sequence data, specifically **Recurrent Neural Networks (RNNs)** and **Long Short-Term Memory (LSTM)** networks.

Our goal was to analyze the `Adj Close` price and develop models capable of predicting the stock's closing price for 1 day, 5 days, and 10 days into the future.

## 2. Approach and Methodology

### 2.1 Data Preprocessing & Exploratory Data Analysis (EDA)
The dataset (`TSLA.csv`) contained historical trading data including Open, High, Low, Close, Adj Close, and Volume. 
- **Feature Selection:** We focused on the `Adj Close` price as the target variable for our predictive models. The `Date` column was converted to a datetime format and set as the index to ensure the time series nature of the data was preserved.
- **Handling Missing Values:** We conducted checks for missing values to ensure the integrity of the time series. (Any missing values in a time series are typically handled via forward-fill or backward-fill interpolation).
- **Data Visualization:** We visualized the historical trends of Tesla's Adjusted Close price to understand the overall market trajectory, noting periods of significant volatility and growth.
- **Data Scaling:** Neural networks are highly sensitive to unscaled input data. We applied `MinMaxScaler` to normalize the stock prices between 0 and 1, ensuring stable and faster convergence during training.
- **Sequence Generation:** To feed data into the SimpleRNN and LSTM models, we implemented a sliding window approach. We used a window of the past $n$ days (e.g., 60 days) to predict the price on day $n+1$.

### 2.2 Deep Learning Modeling
We implemented two distinct architectures using `tensorflow.keras` to compare their performance:

1.  **SimpleRNN Model:** A basic Recurrent Neural Network designed to learn from sequential data. It uses the `SimpleRNN` layer.
2.  **LSTM Model:** Long Short-Term Memory networks are an advanced variant of RNNs. They are specifically designed to overcome the "vanishing gradient" problem of traditional RNNs, allowing them to learn long-term dependencies in the data.

**Common Architectural Elements:**
- Both models utilized a Sequential architecture.
- `Dropout` layers were incorporated to randomly turn off a fraction of neurons during training, preventing overfitting to the training data.
- A final `Dense` layer was used to output the single predicted stock price.
- We used `Mean Squared Error (MSE)` as the loss function and the `Adam` optimizer.
- `EarlyStopping` was used during training to monitor the validation loss and halt training if the model stopped improving, thus avoiding overfitting.

### 2.3 Hyperparameter Tuning
We incorporated a strategy to tune key hyperparameters such as the number of units in the recurrent layers, the dropout rate, and the learning rate using an iterative grid search approach to find the most optimal configuration.

## 3. Results and Model Evaluation
The models were evaluated on an unseen test set. We inversely transformed the scaled predictions to calculate the actual Root Mean Squared Error (RMSE) and Mean Squared Error (MSE).

- **Comparison:** In general, LSTMs tend to outperform SimpleRNNs on financial time series due to their ability to retain long-term historical context, whereas SimpleRNNs are more prone to forgetting earlier data points in a long sequence.
- **Visualization:** A plot overlaying the actual test set prices with the predictions from both the SimpleRNN and the LSTM models was generated to visually assess model fit.

## 4. Insights & Conclusion

**Effectiveness in Capturing Trends:**
The deep learning models (especially LSTM) are generally effective at capturing the broad, macroeconomic trends and momentum of Tesla's stock price. They successfully learn the general upward or downward trajectory over a short-term horizon.

**Limitations:**
- **Sensitivity to Market Fluctuations:** Stock prices are not perfectly deterministic. They are heavily influenced by exogenous variables that are not captured in historical price data alone. The model can struggle with sudden, high-volatility shifts caused by breaking news, earnings reports, or sudden market shocks.
- **Lag Effect:** Often, pure time-series models exhibit a "lag" where their predictions are essentially a slightly shifted version of the previous day's price, particularly in highly unpredictable markets.

**Suggestions for Improvements:**
To build a more robust and accurate trading model, the following enhancements should be considered:
1.  **Alternative Data / Sentiment Analysis:** Incorporate sentiment analysis from financial news headlines, Twitter (X) trends, or Reddit (e.g., r/wallstreetbets) regarding Tesla. Elon Musk's tweets, for example, have historically had immediate impacts on TSLA stock.
2.  **Multivariate Forecasting:** Instead of only using `Adj Close`, include other features like Trading Volume or technical indicators (Moving Averages, RSI, MACD) in the input sequence.
3.  **Macroeconomic Indicators:** Include external data such as interest rates, inflation data, or indices like the S&P 500 or NASDAQ to provide broader market context.
4.  **Advanced Architectures:** Explore newer architectures like GRU (Gated Recurrent Units) or Transformer models, which have shown state-of-the-art performance in time-series forecasting.

## 5. Timeline and Deliverables
- **Data Cleaning & EDA:** Completed
- **Feature Engineering (Sequence Generation):** Completed
- **DL Modelling (SimpleRNN & LSTM):** Completed
- **Model Evaluation:** Completed
- **Final Submission Date:** Projected for Jan 12, 2026

*Attached Deliverable: `Tesla_Stock_Prediction.ipynb` containing the live coding execution.*
