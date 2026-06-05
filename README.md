# 🚗 Tesla Stock Price Predictor

Welcome to the **Tesla Stock Price Predictor**! 

Have you ever wondered if we can predict the future price of a stock? In this project, we built a smart computer program (using Artificial Intelligence) to look at Tesla's past stock prices and guess what the prices will be in the future!

## 🤔 What does this project do?
1. **Reads Past Data:** It looks at Tesla's historical stock prices (like how much the stock cost 5 years ago compared to yesterday).
2. **Learns the Pattern:** It uses two "smart brains" called **LSTM** and **SimpleRNN** (these are Deep Learning models). Think of them as students studying old exam papers to prepare for a future test.
3. **Makes a Guess:** Once the models have learned the pattern, they predict what the stock price will be for the next 1 to 30 days!
4. **Beautiful Interface:** We built a beautiful website (using Streamlit) where anyone can just click a button, generate a forecast, and see beautiful interactive graphs.

## ✨ Features (What's cool about it?)
- **Dynamic & Smooth Charts:** You can zoom in, hover, and play around with the charts (thanks to Plotly!).
- **Search by Date:** Want to know what the predicted price is on a specific day next week? Just use the dropdown to find out!
- **Download Data:** You can download the future predictions directly as a CSV/Excel file.
- **Raw Data Explorer:** You can browse all the past historical data in an interactive table.

## 🛠️ How to run this on your own computer?

It's super easy! Just follow these steps:

1. **Download the Code:** Download or clone this repository.
2. **Install the Requirements:** You need Python installed. Then open your terminal/command prompt and type:
   ```bash
   pip install streamlit pandas numpy matplotlib plotly tensorflow scikit-learn
   ```
3. **Run the App:** In your terminal, type the following command:
   ```bash
   python -m streamlit run app.py
   ```
4. **Enjoy:** A webpage will automatically open in your browser, and you can start predicting!

## 📁 What's inside the folder?
- `app.py`: The main file that runs the website.
- `TSLA.csv`: The Excel file containing all of Tesla's past stock prices.
- `lstm_model.h5` & `rnn_model.h5`: The "smart brains" (pre-trained AI models) that make the predictions.
- `scaler.pkl`: A helper file that scales the numbers so the AI can understand them better.
- `Labmentix_Project_Report.docx`: A detailed project report submitted to Labmentix.

---
*Built with ❤️ and Deep Learning!*
