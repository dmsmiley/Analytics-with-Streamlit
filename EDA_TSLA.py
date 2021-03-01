import pandas as pd
import yfinance as yf
import streamlit as st

#Can be customized with Markdown
st.write("""
# Tesla Stock Price App

Shown are the stock **closing price** and **volume** of Tesla

""")

#define the ticker symbol
tickerSymbol = "TSLA"

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-07-30')

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)

st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)