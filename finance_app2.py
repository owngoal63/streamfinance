import yfinance as yf
import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta


def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['Daily Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['Daily Close'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell)




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

    # Create new data frame to store all the data
    data = pd.DataFrame()
    data['Daily Close'] = tickerDf['Close']
    data['SMA30'] = SMA30['Close']
    data['SMA100'] = SMA100['Close']
    buy_sell_data = buy_sell(data)
    data['Buy Signal Price'] = buy_sell_data[0]
    data['Sell Signal Price'] = buy_sell_data[1]
    # Show the consolidated Dataframe
    #st.dataframe(data)  

    # Visualise the data and the strategy
    fig, ax = plt.subplots()
    ax.plot(data['Daily Close'], label='Daily Close Price ($)', alpha = 0.35)
    ax.plot(data['SMA30'], label='SMA30', alpha = 0.35)
    ax.plot(data['SMA100'], label='SMA100', alpha = 0.35)
    ax.scatter(data.index, data['Buy Signal Price'], label = "Buy", marker='^', color='green')
    ax.scatter(data.index, data['Sell Signal Price'], label = "Sell", marker='v', color='red')
    ax.legend(loc='upper left')
    st.pyplot(fig)


      



