# 📈 Real-Time Stock_Market_Dashboard

A dynamic dashboard built using **Streamlit** to visualize **real-time stock market data** with integrated technical indicators and financial metrics.

## 📌 Description

This project is a **Real-Time Stock Market Dashboard** that allows users to track and analyze stock price movements for multiple companies. The dashboard fetches **live intraday stock data** from the **Alpha Vantage API**, processes it using **Pandas**, and visualizes it with **Plotly**.

The application enables users to:

* Monitor selected stock symbols
* View candlestick price charts
* Analyze **technical indicators** like SMA, EMA, RSI, MACD, and Bollinger Bands
* Review market summaries and key financial metrics
* Toggle between **light** and **dark** modes for user convenience

## 🛠️ Technologies Used

| Technology            | Description                                      |
| --------------------- | ------------------------------------------------ |
| **Python**            | Core language used for development               |
| **Streamlit**         | Framework to build the interactive web dashboard |
| **Pandas**            | For processing and analyzing stock data          |
| **Plotly**            | To create interactive and responsive graphs      |
| **Requests**          | To make API calls to Alpha Vantage               |
| **Alpha Vantage API** | Source of live intraday stock market data        |

## 🚀 Features

* ✅ Multi-stock tracking with custom symbols
* ✅ Configurable time intervals (1min, 5min, 15min, 30min, 60min)
* ✅ Candlestick price charts with optional volume visualization
* ✅ Technical indicators:

  * SMA (Simple Moving Average)
  * EMA (Exponential Moving Average)
  * RSI (Relative Strength Index)
  * MACD (Moving Average Convergence Divergence)
  * Bollinger Bands
* ✅ Market summary table showing:

  * Current price and % change
  * Volume
  * RSI & its interpretation (Overbought/Oversold/Neutral)
  * 52-week High and Low
* ✅ Toggle features like volume, theme (dark/light), and lookback period

## 📷 Dashboard Screens (Features Preview)

> 🖼️ Add screenshots of:
>
> * Price Chart tab
> * Technical Analysis tab
> * Market Summary tab
>   You can use Streamlit’s screenshot or OBS Studio to capture sections.


## 🔑 API Key Setup

1. Create a free account at [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Replace the placeholder API key in your code:

## 🧪 How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/real-time-stock-dashboard.git
cd real-time-stock-dashboard
```

2. Install required libraries:

```bash
pip install streamlit pandas plotly requests
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

> ⚠️ Make sure your internet is connected as it fetches live data from the API.

## 📊 Outcome

A fully functional, interactive web-based **Stock Market Dashboard** that:

* Displays **live financial data** and charts
* Provides **real-time technical analysis**
* Helps users or analysts monitor stock trends at a glance

---

## 💡 Future Improvements

* Add support for historical data visualization
* Add news feed integration using a finance news API
* Enable user authentication for saving watchlists
* Deploy using Streamlit Cloud or Heroku for public access
