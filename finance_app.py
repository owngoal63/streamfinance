import yfinance as yf
import streamlit as st
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta

st.sidebar.header("NYSE Stock Tickers")
tickerSymbols = st.sidebar.multiselect(
    "Select ticker:",
    ["GME", "GOOGL", "JNJ", "AAPL" ,"MSFT", "AMZN", "FB", "BRK-A", "JPM", "XOM", "BAC"],['GME']
)

st.write("""
    # Stock Price Tracker App
    """)

x = st.slider("Move slider to decrease/increase data period in years", min_value=1, max_value=10, value=5) 
start_date = datetime.strftime(datetime.now() - relativedelta(years=x), '%Y-%m-%d')
st.write(x, 'years of data. Start date is ', start_date, '. End date is today. ')


for tickerSymbol in tickerSymbols:
    company_name = yf.Ticker(tickerSymbol).info['longName']
    st.write("""Stock closing prices and volume of """ + company_name  )

    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end='2021-1-29')

    st.line_chart(tickerDf.Close)
    st.line_chart(tickerDf.Volume)
