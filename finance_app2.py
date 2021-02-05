import yfinance as yf
import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta


st.sidebar.header("NYSE Stock Tickers")
tickerSymbols = st.sidebar.multiselect(
    "Select ticker:",
    ["GME", "GOOGL", "JNJ", "AAPL" ,"MSFT", "AMZN", "FB", "BRK-A", "JPM", "XOM", "BAC"],['GME']
)

st.write("""
    # Stock Price Tracker App with Simple Moving Average Tracking
    """)

x = st.slider("Move slider to decrease/increase data period in years", min_value=1, max_value=10, value=5) 
start_date = datetime.strftime(datetime.now() - relativedelta(years=x), '%Y-%m-%d')
st.write(x, 'years of data. Start date is ', start_date, '. End date is today. ')

#Chart setup
plt.style.use('fivethirtyeight')
plt.figure(figsize=(12.5, 4.5))
plt.ylabel("Close Price ($)")
#plt.legend(loc='upper left')


for tickerSymbol in tickerSymbols:
    company_name = yf.Ticker(tickerSymbol).info['longName']
    st.write("""Stock closing prices and volume of """ + company_name  )

    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end='2021-1-29')
    
    # Show the dataframe
    st.dataframe(tickerDf)

    # Create the simple moving average with a 30 day window
    SMA30 = pd.DataFrame()
    SMA30['Close'] = tickerDf['Close'].rolling(window=30).mean()
    #st.dataframe(SMA30)

    # Create the simple moving average with a 30 day window
    SMA100 = pd.DataFrame()
    SMA100['Close'] = tickerDf['Close'].rolling(window=100).mean()
    #st.dataframe(SMA100)

    # Plot the data
    fig, ax = plt.subplots()
    #ax.ticklabel_format(useOffset=False, style='plain')
    ax.plot(tickerDf['Close'], label='Close Price($)')
    ax.plot(SMA30['Close'], label = 'SMA30')
    ax.plot(SMA100['Close'], label = 'SMA100')
    ax.legend(loc='upper left')

    st.pyplot(fig)



