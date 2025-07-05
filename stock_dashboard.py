import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Real-Time Stock Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_KEY = "AIzaSyDaPt13Y_v5j_1_VcA1H9EG5lzzPRmoSuU"  # Replace with your actual Alpha Vantage API key
BASE_URL = "https://www.alphavantage.co/query"

# Cache stock data for 5 minutes to prevent excessive API calls
@st.cache_data(ttl=300)
def get_stock_data(symbol, function="TIME_SERIES_INTRADAY", interval="5min"):
    params = {
        "function": function,
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Process the raw stock data into a clean DataFrame
def process_stock_data(data, interval="5min"):
    if "Time Series (" + interval + ")" not in data:
        return pd.DataFrame()
    
    time_series = data["Time Series (" + interval + ")"]
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df.columns = [col.split(" ")[1] for col in df.columns]
    return df.sort_index()

# Calculate technical indicators
def calculate_technical_indicators(df):
    # Simple Moving Averages
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    
    # Exponential Moving Averages
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    
    # RSI Calculation
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD Calculation
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df['Upper_Band'] = df['SMA_20'] + (2 * df['close'].rolling(window=20).std())
    df['Lower_Band'] = df['SMA_20'] - (2 * df['close'].rolling(window=20).std())
    
    return df

# Main dashboard function
def main():
    st.title("📈 Real-Time Stock Market Dashboard")
    
    # Sidebar controls
    with st.sidebar:
        st.header("Dashboard Configuration")
        
        # Stock symbol input
        default_symbols = "AAPL,MSFT,GOOGL,AMZN"
        symbol_input = st.text_input("Stock Symbols (comma separated)", default_symbols)
        symbols = [s.strip().upper() for s in symbol_input.split(",") if s.strip()]
        
        # Time interval selection
        interval = st.selectbox("Time Interval", ["1min", "5min", "15min", "30min", "60min"])
        
        # Lookback period
        period = st.slider("Lookback Period (days)", 1, 30, 5)
        
        # Technical indicators selection
        st.subheader("Technical Indicators")
        show_sma = st.checkbox("Simple Moving Average (SMA)", True)
        show_ema = st.checkbox("Exponential Moving Average (EMA)", False)
        show_rsi = st.checkbox("Relative Strength Index (RSI)", False)
        show_macd = st.checkbox("Moving Average Convergence Divergence (MACD)", False)
        show_bollinger = st.checkbox("Bollinger Bands", False)
        
        # Display options
        st.subheader("Display Options")
        show_volume = st.checkbox("Show Volume", True)
        dark_mode = st.checkbox("Dark Mode", False)
    
    # Main display area
    if not symbols:
        st.warning("Please enter at least one stock symbol")
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Price Charts", "Technical Analysis", "Market Summary"])
    
    with tab1:
        st.header("Price Charts")
        
        # Create price chart for each symbol
        for symbol in symbols:
            st.subheader(f"{symbol} Price Chart")
            
            # Get and process data
            data = get_stock_data(symbol, interval=interval)
            processed_data = process_stock_data(data, interval)
            
            if processed_data.empty:
                st.error(f"No data available for {symbol}. Please check the symbol or try another one.")
                continue
            
            # Calculate technical indicators if needed
            if any([show_sma, show_ema, show_bollinger]):
                processed_data = calculate_technical_indicators(processed_data)
            
            # Filter data based on selected period
            cutoff_date = datetime.now() - timedelta(days=period)
            filtered_data = processed_data[processed_data.index >= cutoff_date]
            
            # Create main price chart
            fig = go.Figure()
            
            # Candlestick chart
            fig.add_trace(go.Candlestick(
                x=filtered_data.index,
                open=filtered_data['open'],
                high=filtered_data['high'],
                low=filtered_data['low'],
                close=filtered_data['close'],
                name='Price',
                showlegend=False
            ))
            
            # Add technical indicators
            if show_sma:
                fig.add_trace(go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['SMA_20'],
                    name='SMA 20',
                    line=dict(color='orange', width=1)
                ))
                fig.add_trace(go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['SMA_50'],
                    name='SMA 50',
                    line=dict(color='blue', width=1)
                ))
            
            if show_ema:
                fig.add_trace(go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['EMA_12'],
                    name='EMA 12',
                    line=dict(color='green', width=1)
                ))
                fig.add_trace(go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['EMA_26'],
                    name='EMA 26',
                    line=dict(color='red', width=1)
                ))
            
            if show_bollinger:
                fig.add_trace(go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['Upper_Band'],
                    name='Upper Bollinger Band',
                    line=dict(color='gray', width=1, dash='dot')
                ))
                fig.add_trace(go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data['Lower_Band'],
                    name='Lower Bollinger Band',
                    line=dict(color='gray', width=1, dash='dot'),
                    fill='tonexty',
                    fillcolor='rgba(128,128,128,0.1)'
                ))
            
            # Update layout
            fig.update_layout(
                title=f"{symbol} Price ({interval} interval)",
                xaxis_title="Time",
                yaxis_title="Price (USD)",
                hovermode="x unified",
                template="plotly_dark" if dark_mode else "plotly_white",
                height=600,
                xaxis_rangeslider_visible=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume chart if enabled
            if show_volume:
                fig_volume = go.Figure()
                fig_volume.add_trace(go.Bar(
                    x=filtered_data.index,
                    y=filtered_data['volume'],
                    name='Volume',
                    marker_color='rgba(100, 149, 237, 0.6)'
                ))
                fig_volume.update_layout(
                    title=f"{symbol} Trading Volume",
                    xaxis_title="Time",
                    yaxis_title="Volume",
                    template="plotly_dark" if dark_mode else "plotly_white",
                    height=300
                )
                st.plotly_chart(fig_volume, use_container_width=True)
    
    with tab2:
        st.header("Technical Analysis")
        
        for symbol in symbols:
            # Get and process data
            data = get_stock_data(symbol, interval=interval)
            processed_data = process_stock_data(data, interval)
            
            if processed_data.empty:
                continue
            
            # Calculate all technical indicators
            processed_data = calculate_technical_indicators(processed_data)
            
            # Filter data based on selected period
            cutoff_date = datetime.now() - timedelta(days=period)
            filtered_data = processed_data[processed_data.index >= cutoff_date]
            
            # Create columns for each indicator
            col1, col2 = st.columns(2)
            
            with col1:
                # RSI Chart
                if show_rsi:
                    fig_rsi = go.Figure()
                    fig_rsi.add_trace(go.Scatter(
                        x=filtered_data.index,
                        y=filtered_data['RSI'],
                        name='RSI',
                        line=dict(color='purple', width=2)
                    ))
                    fig_rsi.add_hline(y=70, line_dash="dot", line_color="red")
                    fig_rsi.add_hline(y=30, line_dash="dot", line_color="green")
                    fig_rsi.update_layout(
                        title=f"{symbol} RSI (14 periods)",
                        xaxis_title="Time",
                        yaxis_title="RSI Value",
                        template="plotly_dark" if dark_mode else "plotly_white",
                        height=400
                    )
                    st.plotly_chart(fig_rsi, use_container_width=True)
                
                # MACD Chart
                if show_macd:
                    fig_macd = go.Figure()
                    fig_macd.add_trace(go.Scatter(
                        x=filtered_data.index,
                        y=filtered_data['MACD'],
                        name='MACD',
                        line=dict(color='blue', width=2)
                    ))
                    fig_macd.add_trace(go.Scatter(
                        x=filtered_data.index,
                        y=filtered_data['Signal_Line'],
                        name='Signal Line',
                        line=dict(color='orange', width=2)
                    ))
                    fig_macd.update_layout(
                        title=f"{symbol} MACD",
                        xaxis_title="Time",
                        yaxis_title="MACD Value",
                        template="plotly_dark" if dark_mode else "plotly_white",
                        height=400
                    )
                    st.plotly_chart(fig_macd, use_container_width=True)
    
    with tab3:
        st.header("Market Summary")
        
        summary_data = []
        for symbol in symbols:
            data = get_stock_data(symbol, interval=interval)
            processed_data = process_stock_data(data, interval)
            
            if processed_data.empty:
                continue
            
            # Calculate technical indicators for summary metrics
            processed_data = calculate_technical_indicators(processed_data)
            
            # Get latest data point
            latest = processed_data.iloc[-1]
            prev_close = processed_data.iloc[-2]["close"]
            change = latest["close"] - prev_close
            pct_change = (change / prev_close) * 100
            
            # Determine RSI status
            rsi_status = ""
            if 'RSI' in processed_data.columns:
                if latest['RSI'] > 70:
                    rsi_status = "Overbought"
                elif latest['RSI'] < 30:
                    rsi_status = "Oversold"
                else:
                    rsi_status = "Neutral"
            
            summary_data.append({
                "Symbol": symbol,
                "Price": f"${latest['close']:.2f}",
                "Change": f"{change:.2f}",
                "% Change": f"{pct_change:.2f}%",
                "Volume": f"{latest['volume']:,}",
                "RSI (14)": f"{latest.get('RSI', 'N/A'):.2f}",
                "RSI Status": rsi_status,
                "52W High": f"${processed_data['high'].max():.2f}",
                "52W Low": f"${processed_data['low'].min():.2f}"
            })
        
        # Display summary table
        st.dataframe(
            pd.DataFrame(summary_data),
            use_container_width=True,
            hide_index=True
        )
        
        # Display key metrics
        st.subheader("Key Metrics")
        cols = st.columns(len(symbols))
        
        for idx, symbol in enumerate(symbols):
            if idx >= len(cols):
                break
                
            data = get_stock_data(symbol, interval=interval)
            processed_data = process_stock_data(data, interval)
            
            if processed_data.empty:
                continue
                
            processed_data = calculate_technical_indicators(processed_data)
            latest = processed_data.iloc[-1]
            
            with cols[idx]:
                st.metric(
                    label=symbol,
                    value=f"${latest['close']:.2f}",
                    delta=f"{((latest['close'] - processed_data.iloc[-2]['close']) / processed_data.iloc[-2]['close'] * 100):.2f}%"
                )
                
                st.write(f"**Open:** ${latest['open']:.2f}")
                st.write(f"**High:** ${latest['high']:.2f}")
                st.write(f"**Low:** ${latest['low']:.2f}")
                st.write(f"**Volume:** {latest['volume']:,}")
                
                if 'RSI' in processed_data.columns:
                    st.write(f"**RSI (14):** {latest['RSI']:.2f}")
                    if latest['RSI'] > 70:
                        st.error("Overbought")
                    elif latest['RSI'] < 30:
                        st.success("Oversold")
                    else:
                        st.info("Neutral")

# Run the app
if __name__ == "__main__":
    main()