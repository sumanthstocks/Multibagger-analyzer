
import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

# Function to calculate metrics
def calculate_metrics(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y")  # Fetch last 5 years of data

    if df.empty:
        return None

    df["Daily Return"] = df["Close"].pct_change()
    cagr = ((df["Close"].iloc[-1] / df["Close"].iloc[0]) ** (1 / 5) - 1) * 100
    volatility = df["Daily Return"].std() * np.sqrt(252) * 100
    sharpe_ratio = cagr / volatility if volatility != 0 else 0

    return {
        "CAGR (%)": cagr,
        "Volatility (%)": volatility,
        "Sharpe Ratio": sharpe_ratio
    }

# Streamlit App
st.title("Multibagger Stock Analyzer")
st.write("Enter an NSE stock ticker to analyze its potential as a multibagger.")

ticker = st.text_input("Enter NSE stock ticker (e.g., TCS.NS):", "")

if ticker:
    st.write(f"Fetching data for {ticker}...")
    metrics = calculate_metrics(ticker)

    if metrics:
        st.write("### Stock Metrics")
        st.write(f"**CAGR (%):** {metrics['CAGR (%)']:.2f}")
        st.write(f"**Volatility (%):** {metrics['Volatility (%)']:.2f}")
        st.write(f"**Sharpe Ratio:** {metrics['Sharpe Ratio']:.2f}")
    else:
        st.error("No data found for the entered ticker. Please check the ticker and try again.")
