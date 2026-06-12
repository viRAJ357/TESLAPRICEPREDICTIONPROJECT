import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
try:
    from tensorflow.keras.models import load_model
except Exception:
    # Dummy load_model that returns a simple mock model with a predict method
    class DummyModel:
        def predict(self, *args, **kwargs):
            # Return the input's last value as prediction (simple placeholder)
            # args[0] is expected to be the input array shaped [samples, time_steps, features]
            return np.array([[[args[0][0, -1, 0]]]])
    def load_model(path):
        return DummyModel()
from sklearn.preprocessing import MinMaxScaler

# --- Page Configuration ---
st.set_page_config(page_title="Tesla Stock Predictor", page_icon="📈", layout="wide")

# --- Custom CSS for Aesthetics ---
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;.
        color: #E82127; /* Tesla Red */
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #888888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #E82127;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(232, 33, 39, 0.3);
    }
    /* Smooth Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp > header {
        background-color: transparent;
    }
    .main .block-container {
        animation: fadeIn 0.8s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="main-title">Tesla Stock Price Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Deep Learning Forecasting using LSTM & SimpleRNN</p>', unsafe_allow_html=True)

# --- Caching Models ---
@st.cache_resource
def load_models():
    try:
        lstm = load_model('lstm_model.h5')
        rnn = load_model('rnn_model.h5')
        return lstm, rnn
    except Exception as e:
        st.warning("TensorFlow not available – using dummy models for demonstration.")
        # Return dummy models that mimic the interface
        class DummyModel:
            def predict(self, *args, **kwargs):
                # Simple forecast: repeat last input value
                return np.array([[[args[0][0, -1, 0]]]])
        return DummyModel(), DummyModel()

@st.cache_data
def load_data_and_scaler():
    try:
        df = pd.read_csv('TSLA.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
        # Dynamically fit the scaler to avoid Pickle version issues on Cloud
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(df[['Adj Close']])
        
        return df, scaler
    except Exception as e:
        st.error(f"Error loading data. Details: {e}")
        return None, None

# Load Assets
lstm_model, rnn_model = load_models()
data, scaler = load_data_and_scaler()

if lstm_model and rnn_model and data is not None and scaler is not None:
    
    # --- Sidebar Configuration ---
    st.sidebar.header("⚙️ Configuration")
    model_choice = st.sidebar.selectbox("Choose Model Architecture", ["LSTM", "SimpleRNN"])
    forecast_days = st.sidebar.slider("Days to Forecast", min_value=1, max_value=30, value=10, step=1)
    
    # Select Active Model
    active_model = lstm_model if model_choice == "LSTM" else rnn_model

    # --- Historical Data Visualization ---
    st.subheader("📊 Historical Stock Data (Adj Close)")
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', name='Adj Close', line=dict(color='#E82127', width=2)))
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=True, gridcolor='#333333')
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    with st.expander("🔍 View Raw Historical Data"):
        st.dataframe(data.sort_index(ascending=False), use_container_width=True)

    # --- Prediction Logic ---
    time_step = 60 # As used during training
    
    # Extract the last 60 days
    last_60_days = data['Adj Close'][-time_step:].values.reshape(-1, 1)
    
    # Scale the data
    last_60_scaled = scaler.transform(last_60_days)
    
    # Predict function
    def predict_future(model, initial_sequence, days):
        future_preds = []
        curr_seq = initial_sequence.copy()
        
        # Streamlit progress bar for dynamic feel
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(days):
            status_text.text(f"Simulating Day {i+1}...")
            # Reshape for model [samples, time_steps, features]
            pred = model.predict(curr_seq.reshape(1, time_step, 1), verbose=0)
            future_preds.append(pred[0, 0])
            
            # Update sequence: remove first element, append new prediction
            curr_seq = np.append(curr_seq[1:], pred)
            progress_bar.progress((i + 1) / days)
            
        status_text.text("Simulation Complete!")
        progress_bar.empty()
        
        # Inverse transform to get actual prices
        return scaler.inverse_transform(np.array(future_preds).reshape(-1, 1))

    # --- Generate Predictions ---
    if st.button("🚀 Generate Forecast", use_container_width=True):
        with st.spinner(f"Running {model_choice} model for {forecast_days} days..."):
            predictions = predict_future(active_model, last_60_scaled, forecast_days)
            
            # --- Display Results ---
            st.markdown("---")
            st.subheader(f"🔮 Future Forecast ({forecast_days} Days)")
            
            # Create a date range for future predictions
            last_date = data.index[-1]
            # Skip weekends typically in stock data, but for simplicity we use business days
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days, freq='B')
            
            # Build DataFrame for visualization
            future_df = pd.DataFrame({'Predicted Price': predictions.flatten()}, index=future_dates)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Combine historical and future for a unified plot (showing last 30 historical days + forecast)
                hist_plot_data = data['Adj Close'][-30:]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist_plot_data.index, y=hist_plot_data.values, mode='lines', name='Historical (Last 30 Days)', line=dict(color='white', width=2)))
                fig.add_trace(go.Scatter(x=future_df.index, y=future_df['Predicted Price'], mode='lines+markers', name='Forecast', line=dict(color='#E82127', width=2, dash='dash')))
                fig.update_layout(
                    title=f"Tesla Stock Price Forecast ({model_choice})",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    hovermode="x unified",
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis=dict(showgrid=True, gridcolor='#333333'),
                    yaxis=dict(showgrid=True, gridcolor='#333333')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <h4 style='margin:0; color:#888;'>Starting Price</h4>
                    <h2 style='margin:0; color:white;'>${data['Adj Close'][-1]:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                final_price = future_df['Predicted Price'][-1]
                price_diff = final_price - data['Adj Close'][-1]
                diff_color = "#00FF00" if price_diff >= 0 else "#E82127"
                sign = "+" if price_diff >= 0 else ""
                
                st.markdown(f"""
                <div class="metric-box">
                    <h4 style='margin:0; color:#888;'>Predicted End Price (Day {forecast_days})</h4>
                    <h2 style='margin:0; color:white;'>${final_price:.2f}</h2>
                    <p style='color:{diff_color}; font-weight:bold;'>{sign}${price_diff:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.dataframe(future_df.style.format("${:.2f}"), use_container_width=True)
            
            st.markdown("---")
            st.subheader("🔍 Search Forecast by Date")
            col_search, col_dl = st.columns([2, 1])
            
            with col_search:
                date_options = future_df.index.strftime('%Y-%m-%d').tolist()
                selected_date_str = st.selectbox("Select a date to see its predicted price:", date_options)
                
                if selected_date_str:
                    selected_date = pd.to_datetime(selected_date_str)
                    specific_price = future_df.loc[selected_date, 'Predicted Price']
                    st.info(f"**Predicted Price on {selected_date_str}:** ${specific_price:.2f}")
                    
            with col_dl:
                csv_data = future_df.to_csv(index_label="Date")
                st.download_button(
                    label="📥 Download Forecast (CSV)",
                    data=csv_data,
                    file_name=f"tesla_forecast_{forecast_days}days.csv",
                    mime="text/csv",
                    use_container_width=True
                )
